import os
import cv2
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar, QFileDialog, QMessageBox
import utils
import observer

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.createFileMenu()
        self.createEditMenu()
        self.createViewMenu()

        observer.register("checkIfSaved", self.unsaveDataPopupFunction)
        
        self.setGeometry(0, 0, self.parent().width(), 20)
    
    def createFileMenu(self):
        file_menu = self.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.newFunction)
        new_action.setShortcut(QKeySequence.New)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        import_video_action = QAction("Import Video", self)
        import_video_action.triggered.connect(lambda: self.unsaveDataPopupFunction((self.importVideoFunction,lambda: None)))
        import_video_action.setShortcut("Ctrl+I")
        file_menu.addAction(import_video_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save Video", self)
        save_action.triggered.connect(self.saveFunction)
        save_action.setShortcut(QKeySequence.Save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exitFunction)
        file_menu.addAction(exit_action)
    
    def createEditMenu(self):
        edit_menu = self.addMenu("Edit")
        
        recompute_landmarks_action = QAction("Recompute Landmarks", self)
        recompute_landmarks_action.triggered.connect(self.recomputeLandmarksFunction)
        edit_menu.addAction(recompute_landmarks_action)
        
        edit_menu.addSeparator()
        
        add_landmark_action = QAction("Add a Missing Landmark Manually", self)
        add_landmark_action.triggered.connect(self.addLandmarkManuallyFunction)
        edit_menu.addAction(add_landmark_action)
    
    def createViewMenu(self):
        view_menu = self.addMenu("View")
        
        show_face_landmarks_action = QAction("Show/Hide Face Landmarks", self)
        show_face_landmarks_action.triggered.connect(self.showFaceLandmarksFunction)
        view_menu.addAction(show_face_landmarks_action)
        
        show_tooth_landmarks_action = QAction("Show/Hide Tooth Landmarks", self)
        show_tooth_landmarks_action.triggered.connect(self.showToothLandmarksFunction)
        view_menu.addAction(show_tooth_landmarks_action)
        
        show_segments_action = QAction("Show/Hide Segments", self)
        show_segments_action.triggered.connect(self.showSegmentsFunction)
        view_menu.addAction(show_segments_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("Zoom in", self)
        zoom_in_action.triggered.connect(self.zoomInFunction)
        zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom out", self)
        zoom_out_action.triggered.connect(self.zoomOutFunction)
        zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        view_menu.addAction(zoom_out_action)
        
        zoom_to_mouth_action = QAction("Zoom to mouth", self)
        zoom_to_mouth_action.triggered.connect(self.zoomToMouthFunction)
        view_menu.addAction(zoom_to_mouth_action)
        
        view_menu.addSeparator()
        
        enable_mouth_tracking_action = QAction("Enable/Disable mouth tracking", self)
        enable_mouth_tracking_action.triggered.connect(self.enableMouthTrackingFunction)
        view_menu.addAction(enable_mouth_tracking_action)


    def newFunction(self):
        self.parent().resetWindow()

    def importVideoFunction(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import File",
            QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0],
            "Text Files (*.mp4)",
            options=options
        )

        if file_path:
            video = cv2.VideoCapture(file_path)
            videoLenght = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            frames = []
            for _ in range(videoLenght):
                ret, frame = video.read()
                if not ret:
                    print("Error: unable to read video source")
                else : 
                    frames.append(frame)
            data_path = ".".join(file_path.split(".")[:-1] + ["txt"])
            if os.path.isfile(data_path): 
                with open(data_path, 'r') as file:
                    landmarks,intervals = utils.strToDataList(file.read())
                observer.update("dataSaved", True)
            else:
                QMessageBox.warning(
                self,
                "Warning",
                "The imported video has no associated data file !\nThe face landmarks will be computed with a constant framerate.\nTake care of the results !",
                QMessageBox.Ok
                )
                landmarks = utils.faceMeshProcess(frames)
                intervals = [1000/video.get(cv2.CAP_PROP_FPS) for _ in range(videoLenght)]
                observer.update("dataSaved", False)
            observer.update("videoSaved", True)
            observer.update("loadedFrames", [frames, intervals])
            observer.update("faceLandmarks", landmarks)
            observer.update("videoLoaded", True)

    def saveFunction(self):
        if not observer.get("videoLoaded"):
            QMessageBox.warning(
                self,
                "Error",
                "No video recorded yet",
                QMessageBox.Ok
            )
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video",
            QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0],
            "All Files (*)",
            options=options
        )

        if file_path:
            if os.path.isfile(file_path):
                QMessageBox.warning(
                self,
                "Error",
                "A file with the same name already exists",
                QMessageBox.Ok
                )
                return
            if os.path.isdir(file_path): os.remove(file_path)
            os.mkdir(file_path)

            video_path = os.path.join(file_path, os.path.basename(file_path) + ".mp4")
            data_path = os.path.join(file_path, os.path.basename(file_path) + ".txt")

            frames,intervals = observer.get("loadedFrames")
            landmarks = observer.get("faceLandmarks")

            frame_height, frame_width = frames[0].shape[:2]
            output_fps = 1000/(sum(intervals)/len(intervals))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            out = cv2.VideoWriter(video_path, fourcc, output_fps, (frame_width, frame_height))
            [out.write(frame) for frame in frames]
            out.release()

            with open(data_path, 'w') as file:
                file.write(utils.dataListToStr(landmarks, intervals))

            observer.update("videoSaved", True)
            observer.update("dataSaved", True)
    
    def exitFunction(self):
        self.parent().close()

    def recomputeLandmarksFunction(self):
        if observer.get("videoLoaded"):
            faceLandmarks = utils.faceMeshProcess(observer.get("loadedFrames")[0])
            observer.update("faceLandmarks", faceLandmarks)
            observer.update("dataSaved", False)

    def addLandmarkManuallyFunction(self):
        pass

    def showFaceLandmarksFunction(self):
        observer.update("showLandmarks", not observer.get("showLandmarks"))
        self.parent().camera.update()

    def showToothLandmarksFunction(self):
        pass

    def showSegmentsFunction(self):
        pass

    def zoomInFunction(self):
        observer.update("zoom", observer.get("zoom") + 0.1)
        self.parent().camera.update()

    def zoomOutFunction(self):
        observer.update("zoom", observer.get("zoom") - 0.1)
        self.parent().camera.update()

    def zoomToMouthFunction(self):
        landmarks = observer.get("faceLandmarks")[observer.get("framePosition")]
        h,w = self.parent().camera.currentFrame.shape[:2]
        nw = (landmarks[291][0]-landmarks[61][0])*w*4
        nh = (landmarks[17][1]-landmarks[0][1])*h*2
        if not observer.get("mouthTracking") : 
            observer.update("mouthTracking", True)
        observer.update("zoom", round(min(w/nw, h/nh),1))
        self.parent().camera.update()

    def enableMouthTrackingFunction(self):
        observer.update("mouthTracking", not observer.get("mouthTracking"))
        self.parent().camera.update()

    def unsaveDataPopupFunction(self, actions):
        if observer.get("videoLoaded") and (not observer.get("videoSaved") or not observer.get("dataSaved")):
            confirm = QMessageBox.question(
            self,
            "Confirmation",
            "Some video or data are not saved.\nAre you sure to continue ?",
            QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                actions[0]()
            else:
                actions[1]()
        else:
            actions[0]()

    

    

