import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QApplication

class CurvesWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Curves")

    # def comboBox(self):

        # self.parameter = QLabel('Lip Lenth',self)

        combo = QComboBox(self)

        combo.addItem('Lip Lenth')
        combo.addItem('Upper Lip Thickness')
        combo.addItem('Lower Lip Thickness')
        combo.addItem('Interlabial Gap')
        combo.addItem('Commissure Corridor Left')
        combo.addItem('Commissure Corridor Right')
        combo.addItem('Smile Width')
        combo.addItem('Smile Index')

        combo.move(0,50)
        # self.parameter.move(50)

        self.show


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor("white"))