import sys
import os
import cv2
from PySide6 import QtCore, QtWidgets

import observer
import camera
import player
import datasheet
import curves
import menubar

window = None

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.resize(800, 600)

        self.mainLayout = QtWidgets.QHBoxLayout(self, contentsMargins=QtCore.QMargins(0, 0, 0, 0))
        
        # Create the splitter
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        
        # Create the frames on each side
        self.leftFrame = QtWidgets.QWidget()
        self.rightFrame = QtWidgets.QWidget()
        
        # Set layouts for the frames
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftFrame, contentsMargins=QtCore.QMargins(0, 0, 0, 0), spacing=0)
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightFrame, contentsMargins=QtCore.QMargins(0, 0, 0, 0), spacing=0)
        
        # Add widgets or other layouts to the left frame
        self.combo_box = camera.CameraSelector()
        self.camera = camera.CameraWidget()
        self.playToolbar = player.PlayerWidget()
        # set expanding horizontally and rap contant vertically
        self.leftLayout.addWidget(self.combo_box, alignment=QtCore.Qt.AlignTop)
        self.leftLayout.addWidget(self.camera)
        self.leftLayout.addWidget(self.playToolbar, alignment=QtCore.Qt.AlignCenter)
        
        # Add widgets or other layouts to the right frame
        self.dataSheet = datasheet.DataSheetWidget()
        self.curves = curves.CurvesWidget()
        self.rightLayout.addWidget(self.dataSheet)
        self.rightLayout.addWidget(self.curves)
        
        # Add the frames to the splitter
        self.splitter.addWidget(self.leftFrame)
        self.splitter.addWidget(self.rightFrame)
        
        # Add the splitter to the main layout
        self.mainLayout.addWidget(self.splitter)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        windowWidth = self.width()
        self.splitter.setSizes([int(windowWidth*0.7), int(windowWidth*0.3)])
        self.menubar = menubar.MenuBar(self)
        observer.update("isResizing", False)

    def resetWindow(self):
        self.close()
        createMainWindow()

    def closeEvent(self, event):
        self.menubar.unsaveDataPopupFunction((
            lambda self=self: (
                setattr(self.camera,"stopThread",True),
                self.camera.video_capture.release(),
                event.accept()),
            event.ignore))

def createMainWindow():
    global window
    observer.resetAllData()
    window = MainWindow()
    window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    createMainWindow()

    sys.exit(app.exec())