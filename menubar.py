
import os
import shutil
import pickle
import imageio
from PySide6 import QtWidgets,QtGui,QtCore
import facemesh
import observer

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.createFileMenu()
        self.createEditMenu()
        self.createViewMenu()
        
        self.setGeometry(0, 0, self.parent().width(), 20)
    
    def createFileMenu(self):
        file_menu = self.addMenu("File")
        
        new_action = QtGui.QAction("New", self)
        new_action.triggered.connect(self.newFunction)
        new_action.setShortcut(QtGui.QKeySequence.New)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        import_video_action = QtGui.QAction("Import Video", self)
        import_video_action.triggered.connect(self.importVideoFunction)
        import_video_action.setShortcut("Ctrl+I")
        file_menu.addAction(import_video_action)
        
        file_menu.addSeparator()
        
        save_action = QtGui.QAction("Save Video", self)
        save_action.triggered.connect(self.saveFunction)
        save_action.setShortcut(QtGui.QKeySequence.Save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QtGui.QAction("Exit", self)
        exit_action.triggered.connect(self.exitFunction)
        file_menu.addAction(exit_action)
    
    def createEditMenu(self):
        edit_menu = self.addMenu("Edit")
        
        recompute_landmarks_action = QtGui.QAction("Recompute Landmarks", self)
        recompute_landmarks_action.triggered.connect(self.recomputeLandmarksFunction)
        edit_menu.addAction(recompute_landmarks_action)
        
        edit_menu.addSeparator()
        
        add_landmark_action = QtGui.QAction("Add a Missing Landmark Manually", self)
        add_landmark_action.triggered.connect(self.addLandmarkManuallyFunction)
        edit_menu.addAction(add_landmark_action)
    
    def createViewMenu(self):
        view_menu = self.addMenu("View")
        
        show_face_landmarks_action = QtGui.QAction("Show/Hide Face Landmarks", self)
        show_face_landmarks_action.triggered.connect(self.showFaceLandmarksFunction)
        view_menu.addAction(show_face_landmarks_action)
        
        show_tooth_landmarks_action = QtGui.QAction("Show/Hide Tooth Landmarks", self)
        show_tooth_landmarks_action.triggered.connect(self.showToothLandmarksFunction)
        view_menu.addAction(show_tooth_landmarks_action)
        
        show_segments_action = QtGui.QAction("Show/Hide Segments", self)
        show_segments_action.triggered.connect(self.showSegmentsFunction)
        view_menu.addAction(show_segments_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QtGui.QAction("Zoom in", self)
        zoom_in_action.triggered.connect(self.zoomInFunction)
        zoom_in_action.setShortcut(QtGui.QKeySequence.ZoomIn)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QtGui.QAction("Zoom out", self)
        zoom_out_action.triggered.connect(self.zoomOutFunction)
        zoom_out_action.setShortcut(QtGui.QKeySequence.ZoomOut)
        view_menu.addAction(zoom_out_action)
        
        zoom_to_mouth_action = QtGui.QAction("Zoom to mouth", self)
        zoom_to_mouth_action.triggered.connect(self.zoomToMouthFunction)
        view_menu.addAction(zoom_to_mouth_action)
        
        view_menu.addSeparator()
        
        enable_mouth_tracking_action = QtGui.QAction("Enable/Disable mouth tracking", self)
        enable_mouth_tracking_action.triggered.connect(self.enableMouthTrackingFunction)
        view_menu.addAction(enable_mouth_tracking_action)


    def newFunction(self):
        self.unsaveDataPopupFunction(self.parent().resetWindow, lambda: None)

    def importVideoFunction(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Import File",
            QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0],
            "Text Files (*.mp4)",
            options=options
        )

        if file_path:
            video = imageio.get_reader(file_path)
            frames = [video.get_data(i) for i in range(video.count_frames())]
            intervals = video.get_meta_data()
            observer.update("loadedFrames", [frames, intervals['frame_intervals']])
            observer.update("videoLoaded", True)
            data_path = ".".join(file_path.split(".")[:-1] + ["pkl"])
            if os.path.isfile(data_path): 
                with open(data_path, 'rb') as file:
                    observer.update("faceLandmarks",pickle.load(file))  
            else:
                observer.update("faceLandmarks", facemesh.faceMeshProcess("output.avi"))

    def saveFunction(self):
        if not observer.get("videoLoaded"):
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "No video recorded yet",
                QtWidgets.QMessageBox.Ok
            )
            return

        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Video",
            QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0],
            "MP4 Files (*.mp4)","All Files (*)",
            options=options
        )
        
        if file_path:
            if os.path.isfile(file_path):
                QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "A file with the same name already exists",
                QtWidgets.QMessageBox.Ok
                )
                return
            if os.path.isdir(file_path): os.remove(file_path)
            os.mkdir(file_path)
            frames,intervals = observer.get("loadedFrames")
            fps = 1000/(sum(intervals)/len(intervals))
            imageio.mimwrite(os.path.join(file_path,os.path.basename(file_path)+".mp4"), frames, fps=fps, metadata={'frame_intervals': 'intervals'})
            data_path = os.path.join(file_path,os.path.basename(file_path)+".pkl")
            with open(data_path, 'wb') as file:
                pickle.dump(observer.get("faceLandmarks"), file)
            observer.update("videoSaved", True)
    
    def exitFunction(self):
        self.parent().close()

    def recomputeLandmarksFunction(self):
        if observer.get("videoLoaded"):
            facemesh.faceMeshProcess(observer.get("loadedFrames"))

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
        pass

    def enableMouthTrackingFunction(self):
        observer.update("mouthTracking", not observer.get("mouthTracking"))
        self.parent().camera.update()

    def unsaveDataPopupFunction(self, yesAction, noAction):
        if observer.get("videoLoaded") and (not observer.get("videoSaved") or not observer.get("dataSaved")):
            confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Some video or data are not saved\nAre you sure you want to continue ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                yesAction()
            else:
                noAction()

    

    

