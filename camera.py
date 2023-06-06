import cv2
from PySide6 import QtCore, QtWidgets, QtGui
import mediapipe as mp
import observer

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
        self.timer.timeout.connect(self.loadNextFrame)
        self.timer.start(33)

        self.currentFrame = None
        self.writeFrame = lambda frame,landmarks: None
        self.loadNextFrame()

        observer.update("videoLoaded", False)
        observer.register("isRecording", self.startRecord)
        observer.register("videoLoaded", self.changeVideoCapture)
        observer.register("isPlaying", self.playLoadedVideo)
        observer.register("previousFrame", lambda _: self.previousFrame())
        observer.register("nextFrame", lambda _: self.nextFrame())
        observer.register("goToStart", lambda _: self.toStart())
        observer.register("goToEnd", lambda _: self.toEnd())
        observer.register("framePosition", self.updateStartEndObserver)
        observer.update("videoLength", 0)
        observer.update("faceLandmarks", self.faceLandmarks)

    def paintEvent(self, event):
        image = self.currentFrame.copy()
        face_landmarks = self.faceLandmarks[observer.get("framePosition")]
        if face_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_tesselation_style())
        image = self.convert_frame_to_image(image)
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor("black"))
        painter.drawImage(self.rect().center() - image.rect().center(), image)
    
    def convert_frame_to_image(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = channel * width
        q_image = QtGui.QImage(cv2.flip(frame, 1).data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        q_image = q_image.scaledToHeight(self.height())
        return q_image.rgbSwapped()

    def changeVideoCapture(self, videoLoaded):
        self.video_capture.release()
        if videoLoaded:
            self.video_capture = cv2.VideoCapture("output.avi")
            videoLength = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            observer.update("videoLength", videoLength)
            observer.update("frameLandmarks", [None]*(videoLength+1))
            observer.update("isPlaying", False)
            self.loadNextFrame()
        else:
            self.video_capture = cv2.VideoCapture(0)

    def playLoadedVideo(self, isPlaying):
        if not observer.get("videoLoaded"): return
        if isPlaying:
            observerIndex = observer.register("isAtEnd", 
                lambda isAtEnd: (observer.update("isPlaying",False), 
                                 observer.update("goToStart",None),
                                 observer.unregister("isAtEnd",observerIndex)) 
                                 if isAtEnd else None)
            self.timer.start(33)
        else:
            self.timer.stop()

    def previousFrame(self):
        if not observer.get("videoLoaded"): return
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_capture.get(cv2.CAP_PROP_POS_FRAMES) - 2)
        self.loadNextFrame()

    def nextFrame(self):
        if not observer.get("videoLoaded"): return
        self.loadNextFrame()

    def toStart(self):
        if not observer.get("videoLoaded"): return
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.loadNextFrame()
    
    def toEnd(self):
        if not observer.get("videoLoaded"): return
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        self.loadNextFrame()

    def startRecord(self, record):
        if not record: return
        w = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 33.0, (w,h))
        self.writeFrame = lambda frame,landmarks: (videoWriter.write(frame), self.faceLandmarks.append(landmarks))
        observerIndex = observer.register("isRecording", lambda record: self.stopRecord(videoWriter,observerIndex) if not record else None)

    def stopRecord(self, videoWriter, observerIndex):
        videoWriter.release()
        observer.unregister("isRecording", observerIndex)
        observer.update("videoLoaded", True)
        self.writeFrame = lambda frame,landmarks: None

    def loadNextFrame(self):
        if not self.video_capture.isOpened():
            print("Error: unable to open video source")
        else :
            ret, frame = self.video_capture.read()
            if not ret:
                print("Error: unable to read video source")
            else : 
                self.currentFrame = frame
                framePosition = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
                observer.update("framePosition", framePosition)
                # face mesh
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(frame).multi_face_landmarks
                #live result
                if results and framePosition == 0:
                    self.faceLandmarks[framePosition] = results[0]
                    observer.update("faceLandmarks", self.faceLandmarks)
                    print(observer.get("faceLandmarks")[framePosition].landmark[0].x)
            self.update()
        self.writeFrame(self.currentFrame, results[0] if results else None)

    def updateStartEndObserver(self, pos):
        IsAtStart, isAtEnd = pos == 1, pos == observer.get("videoLength")
        observer.update("isAtStart", IsAtStart) if IsAtStart != observer.get("isAtStart") else None
        observer.update("isAtEnd", isAtEnd) if isAtEnd != observer.get("isAtEnd") else None
        


    



