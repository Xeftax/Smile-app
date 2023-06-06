
import sys
from PySide6 import QtWidgets,QtGui,QtCore
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
        
        save_video_action = QtGui.QAction("Save Video", self)
        save_video_action.triggered.connect(self.saveVideoFunction)
        file_menu.addAction(save_video_action)
        
        save_landmarks_action = QtGui.QAction("Save Landmarks", self)
        save_landmarks_action.triggered.connect(self.saveLandmarksFunction)
        file_menu.addAction(save_landmarks_action)
        
        save_all_action = QtGui.QAction("Save All", self)
        save_all_action.triggered.connect(self.saveAllFunction)
        save_all_action.setShortcut(QtGui.QKeySequence.Save)
        file_menu.addAction(save_all_action)
        
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

        view_menu.addSeparator()

        add_missing_landmark_action = QtGui.QAction("Add a Missing Landmark Manually", self)
        add_missing_landmark_action.triggered.connect(self.addMissingLandmarkFunction)
        view_menu.addAction(add_missing_landmark_action)

    def newFunction(self):
        self.unsaveDataPopupFunction(self.parent().resetWindow, lambda: None)

    def importVideoFunction(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Import File",
            QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0],
            "Text Files (*.avi);;All Files (*)",
            options=options
        )
        
        if file_path:
            print("Selected File:", file_path)

    def saveVideoFunction(self):
        pass

    def saveLandmarksFunction(self):
        pass

    def saveAllFunction(self):
        pass

    def exitFunction(self):
        self.parent().close()

    def recomputeLandmarksFunction(self):
        pass

    def addLandmarkManuallyFunction(self):
        pass

    def showFaceLandmarksFunction(self):
        pass

    def showToothLandmarksFunction(self):
        pass

    def showSegmentsFunction(self):
        pass

    def zoomInFunction(self):
        pass

    def zoomOutFunction(self):
        pass

    def zoomToMouthFunction(self):
        pass

    def enableMouthTrackingFunction(self):
        pass

    def addMissingLandmarkFunction(self):
        pass

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

    

    

