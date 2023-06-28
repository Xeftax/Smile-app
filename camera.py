import time
import cv2
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
import mediapipe as mp
import utils
import observer
import threading

class CameraWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #Face recognition
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.faceLandmarks = [None]

        #Video capture
        self.video_capture = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.loadNextLiveFrame)
        self.timer.start(33)

        self.currentFrame = None
        self.framePosition = None
        self.recordedFrames = [[],[]] # [frames, frameInterval]
        self.prevFrameTime = None
        self.recordFrame = lambda _: None
        self.drawFrameLandmarks = lambda _: None
        self.imageCenter = None
        self.zoom_factor = 1.0
        self.time = [0]
        self.loadNextLiveFrame()

        self.stopThread = False
        threading.Thread(target=self.liveResult).start()

        observer.register("isRecording", self.startRecord)
        observer.register("videoLoaded", self.changeVideoCapture)
        observer.register("isPlaying", self.playLoadedVideo)
        observer.register("previousFrame", lambda _: self.previousFrame())
        observer.register("nextFrame", lambda _: self.nextFrame())
        observer.register("goToStart", lambda _: self.toStart())
        observer.register("goToEnd", lambda _: self.toEnd())
        observer.register("framePosition", self.updateStartEndObserver)
        observer.register("faceLandmarks", lambda faceLandmarks, self=self: setattr(self, 'faceLandmarks', faceLandmarks))
        observer.register("showLandmarks", lambda showLandmarks, self=self: setattr(self, 'drawFrameLandmarks', self.drawLandmarks) if showLandmarks else setattr(self, 'drawFrameLandmarks', lambda _: None))
        observer.register("zoom", lambda zoom, self=self: setattr(self,"zoom_factor",zoom))
        observer.register("framePosition", self.mouthTracking)
        observer.register("loadedFrames", lambda frames, self=self: setattr(self,"recordedFrames",frames))

        observer.update("videoLoaded", False)
        observer.update("videoLength", 0)
        observer.update("isAtStart", False)
        observer.update("isAtEnd", False)
        observer.update("faceLandmarks", self.faceLandmarks)
        observer.update("showLandmarks", True)
        observer.update("zoom", self.zoom_factor)
        observer.update("mouthTracking", False)
        observer.update("videoSaved", False)
        observer.update("dataSaved", False)

    def paintEvent(self, event):
        image = self.currentFrame.copy()
        self.drawFrameLandmarks(image)
        w,h = image.shape[1]/self.zoom_factor, image.shape[0]/self.zoom_factor
        if not self.imageCenter: self.mouthTracking(0)
        x1 = int(self.imageCenter[0]-w/2)
        x2 = int(self.imageCenter[0]+w/2)
        y1 = int(self.imageCenter[1]-h/2)
        y2 = int(self.imageCenter[1]+h/2)
        if x1 < 0:
            x2 += x1
            x1 = 0
        elif x2 > image.shape[1]:
            x1 += x2 - image.shape[1]
            x2 = image.shape[1]
        if y1 < 0:
            y2 += y1
            y1 = 0
        elif y2 > image.shape[0]:
            y1 += y2 - image.shape[0]
            y2 = image.shape[0]
        image = image[y1:y2, x1:x2]
        convertedImage = self.convert_frame_to_image(image)
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor("black"))
        painter.drawImage(self.rect().center() - convertedImage.rect().center(), convertedImage)

    def wheelEvent(self, event):
        modifiers = QtGui.QGuiApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_factor *= 1.1  # Increase zoom factor
            else:
                self.zoom_factor /= 1.1  # Decrease zoom factor
            if self.zoom_factor < 1.0:
                self.zoom_factor = 1.0
            if self.zoom_factor > 10.0:
                self.zoom_factor = 10.0
            observer.update("zoom", self.zoom_factor)
            self.update()
    
    def convert_frame_to_image(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = channel * width
        q_image = QtGui.QImage(np.ascontiguousarray(frame.data), width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        q_image = q_image.scaledToHeight(self.height())
        return q_image.rgbSwapped()

    def changeVideoCapture(self, videoLoaded):
        self.video_capture.release()
        if videoLoaded:
            self.timer.timeout.disconnect()
            self.timer.timeout.connect(self.loadNextRecordedFrame)
            observer.update("videoLength", len(self.recordedFrames[0]))
            observer.update("isPlaying", False)
            self.toStart()
        else:
            self.timer.timeout.disconnect()
            self.timer.timeout.connect(self.loadNextLiveFrame)
            self.timer.start(33)
            self.video_capture = cv2.VideoCapture(0)

    def playLoadedVideo(self, isPlaying):
        if not observer.get("videoLoaded"): return
        if isPlaying:
            if observer.get("isAtEnd"): self.toStart()
            observerIndex = observer.register("isAtEnd", 
                lambda isAtEnd: (observer.update("isPlaying",False), 
                                 observer.unregister("isAtEnd",observerIndex)) 
                                 if isAtEnd else None)
            self.timer.start(self.recordedFrames[1][observer.get("framePosition")])
        else:
            self.timer.stop()

    def previousFrame(self):
        if not observer.get("videoLoaded"): return
        observer.update("framePosition", observer.get("framePosition") - 2)
        self.loadNextRecordedFrame()

    def nextFrame(self):
        if not observer.get("videoLoaded"): return
        self.loadNextRecordedFrame()

    def toStart(self):
        if not observer.get("videoLoaded"): return
        observer.update("framePosition", -1)
        self.loadNextRecordedFrame()
    
    def toEnd(self):
        if not observer.get("videoLoaded"): return
        observer.update("framePosition", observer.get("videoLength")-2)
        self.loadNextRecordedFrame()

    def startRecord(self, record):
        if not record: return
        observer.update("createNew",None)
        self.recordFrame = self.saveFrame
        observerIndex = observer.register("isRecording", lambda record: self.stopRecord(observerIndex) if not record else None)

    def stopRecord(self, observerIndex):
        observer.unregister("isRecording", observerIndex)
        observer.update("loadedFrames", self.recordedFrames)
        observer.update("videoLoaded", True)
        self.recordFrame = lambda _: None
        self.faceLandmarks = utils.faceMeshProcess(self.recordedFrames[0])
        observer.update("faceLandmarks", self.faceLandmarks)

    def loadNextLiveFrame(self):
        if not self.video_capture.isOpened():
            print("Error: unable to open video source")
        else :
            ret, frame = self.video_capture.read()
            if not ret:
                print("Error: unable to read video source")
            else : 
                frame = cv2.flip(frame, 1)
                self.currentFrame = frame
                observer.update("framePosition", 0)
            self.update()
        self.recordFrame(frame)

    def loadNextRecordedFrame(self):
        framePosition = observer.get("framePosition")+1
        self.currentFrame = self.recordedFrames[0][framePosition]
        observer.update("framePosition", framePosition)
        if observer.get("isPlaying"): self.timer.start(self.recordedFrames[1][framePosition])
        self.update()

    def saveFrame(self, frame):
        currentTime = time.time()
        interval = (currentTime - self.prevFrameTime if self.prevFrameTime else 0)*1000
        self.prevFrameTime = currentTime
        self.recordedFrames[0].append(frame)
        self.recordedFrames[1].append(interval)

    def mouthTracking(self,framePosition):
        h,w = self.currentFrame.shape[:2]
        if observer.get("mouthTracking"): 
            x1 = self.faceLandmarks[framePosition][61][0]*w
            x2 = self.faceLandmarks[framePosition][291][0]*w
            y1 = self.faceLandmarks[framePosition][0][1]*h
            y2 = self.faceLandmarks[framePosition][17][1]*h
            self.imageCenter = (int((x1 + x2)/2), int((y1 + y2)/2))
        else:
            self.imageCenter = (int(w/2), int(h/2))

    def liveResult(self):
        while not observer.get("videoLoaded") and not self.stopThread:
            results = self.face_mesh.process(self.currentFrame).multi_face_landmarks
            if results: 
                self.faceLandmarks[0] = [[l.x,l.y,l.z] for l in results[0].landmark]
                observer.update("faceLandmarks", self.faceLandmarks)

    def drawLandmarks(self,image):
        face_landmarks = self.faceLandmarks[observer.get("framePosition")]
        if not face_landmarks: return
        for landmark in face_landmarks:
            x = int(landmark[0] * image.shape[1])
            y = int(landmark[1] * image.shape[0])
            cv2.circle(image, (x, y), 1, (200, 200, 200), -1)

    def updateStartEndObserver(self, pos):
        IsAtStart, isAtEnd = pos == 0, pos == observer.get("videoLength")-1
        if IsAtStart != observer.get("isAtStart") :
            observer.update("isAtStart", IsAtStart)
        if isAtEnd != observer.get("isAtEnd"):
            observer.update("isAtEnd", isAtEnd)

        


    



