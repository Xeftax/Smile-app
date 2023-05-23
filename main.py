import sys
from PySide6 import QtCore, QtWidgets, QtGui

import camera
import player
import datasheet
import curves

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        
        # Create the splitter
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        
        # Create the frames on each side
        self.leftFrame = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.StyledPanel)
        self.rightFrame = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.StyledPanel)
        
        # Set layouts for the frames
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftFrame)
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightFrame)
        
        # Add widgets or other layouts to the left frame
        self.camera = camera.CameraWidget()
        self.playToolbar = player.PlayerWidget()
        self.playToolbar.setFixedHeight(50)
        self.leftLayout.addWidget(self.camera)
        self.leftLayout.addWidget(self.playToolbar)
        
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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.splitter.setSizes([int(widget.splitter.size().width()*0.7), int(widget.splitter.size().width()*0.3)])
    widget.show()

    sys.exit(app.exec())