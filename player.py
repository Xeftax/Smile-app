from os import path
from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon
import observer

btnSize = 50

class PlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self, contentsMargins=QMargins(0, 0, 0, 0))

        iconDir = "resources"
        toStartButton = IconButton(QIcon(path.join(iconDir,"to_start_icon.svg")), "goToStart", (["videoLoaded","isAtStart"],[True,False]))
        previousButton = IconButton(QIcon(path.join(iconDir,"previous_icon.svg")), "previousFrame", (["videoLoaded","isAtStart"],[True,False]))
        playButton = ToggleButton(QIcon(path.join(iconDir,"play_icon.svg")), QIcon(path.join(iconDir,"pause_icon.svg")), "isPlaying",(["videoLoaded"],[True]))
        nextButton = IconButton(QIcon(path.join(iconDir,"next_icon.svg")), "nextFrame", (["videoLoaded","isAtEnd"],[True,False]))
        toEndButton = IconButton(QIcon(path.join(iconDir,"to_end_icon.svg")), "goToEnd", (["videoLoaded","isAtEnd"],[True,False]))
        blank = QWidget()
        blank.setFixedWidth(30)
        recordButton = ToggleButton(QIcon(path.join(iconDir,"record_icon.svg")), QIcon(path.join(iconDir,"stop_icon.svg")), "isRecording")
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


class IconButton(QPushButton):
    def __init__(self, icon, observerName, enableConditions=([],[])):
        super().__init__(icon, "")
        
        self.setCheckable(False)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(btnSize, btnSize)

        self.conditionState = enableConditions[1][:]
        for i,condition in enumerate(enableConditions[0]):
            self.conditionState[i] = observer.get(condition)
            observer.register(condition, lambda state, i=i: (self.conditionState.__setitem__(i, state), self.setEnabled(self.conditionState == enableConditions[1])))
        self.setEnabled(self.conditionState == enableConditions[1])

        self.clicked.connect(lambda: self.onClick(observerName))

    def onClick(self, observerName):
        observer.update(observerName, None)
        

class ToggleButton(IconButton):
    def __init__(self, icon1, icon2, observerName, observerLimit=([],[])):
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


        

    