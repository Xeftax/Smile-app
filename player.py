from PySide6 import QtCore, QtWidgets, QtGui
from os import path
import observer

btnSize = 50

class PlayerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self, contentsMargins=QtCore.QMargins(0, 0, 0, 0))

        iconDir = "resources"
        toStartButton = IconButton(QtGui.QIcon(path.join(iconDir,"to_start_icon.svg")), "goToStart", "isAtStart")
        previousButton = IconButton(QtGui.QIcon(path.join(iconDir,"previous_icon.svg")), "previousFrame", "isAtStart")
        playButton = ToggleButton(QtGui.QIcon(path.join(iconDir,"play_icon.svg")), QtGui.QIcon(path.join(iconDir,"pause_icon.svg")), "isPlaying")
        nextButton = IconButton(QtGui.QIcon(path.join(iconDir,"next_icon.svg")), "nextFrame", "isAtEnd")
        toEndButton = IconButton(QtGui.QIcon(path.join(iconDir,"to_end_icon.svg")), "goToEnd", "isAtEnd")
        blank = QtWidgets.QWidget()
        blank.setFixedWidth(30)
        recordButton = ToggleButton(QtGui.QIcon(path.join(iconDir,"record_icon.svg")), QtGui.QIcon(path.join(iconDir,"stop_icon.svg")), "isRecording")
        recordButton.setEnabled(True)

        layout.addWidget(toStartButton)
        layout.addWidget(previousButton)
        layout.addWidget(playButton)
        layout.addWidget(nextButton)
        layout.addWidget(toEndButton)
        layout.addWidget(blank)
        layout.addWidget(recordButton)

        self.setFixedHeight(btnSize)
        self.setFixedWidth(7*(btnSize + 10) + 10)     


class IconButton(QtWidgets.QPushButton):
    def __init__(self, icon, observerUpdate, observerLimit=None):
        super().__init__(icon, "")
        
        self.setCheckable(False)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedSize(btnSize, btnSize)

        self.setEnabled(observer.get("videoLoaded"))
        observer.register("videoLoaded", lambda state: self.setEnabled(state and not observer.get(observerLimit)))
        if observerLimit: observer.register(observerLimit, lambda state: self.setEnabled(not state and observer.get("videoLoaded")))

        self.clicked.connect(lambda: self.onClick(observerUpdate))

    def onClick(self, observerName):
        observer.update(observerName, None)
        

class ToggleButton(IconButton):
    def __init__(self, icon1, icon2, observerName, observerLimit=None):
        super().__init__(icon1, observerName, observerLimit)
        
        self.setCheckable(True)

        observer.update(observerName, False)
        observer.register(observerName, lambda state: self.toggleDisplay(icon1, icon2, state))

    def onClick(self, observerName):
        observer.update(observerName, self.isChecked())
    
    def toggleDisplay(self, icon1, icon2, state):
        if state:
            self.setChecked(True)
            self.setIcon(icon2) 
        else:
            self.setChecked(False)
            self.setIcon(icon1)


        

    