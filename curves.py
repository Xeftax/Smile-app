import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QApplication, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtCore import Qt, QTimer
import datasheet
import observer

class CurvesWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Curves")

        layout = QVBoxLayout()
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        self.chart = QChart()
        self.series = QLineSeries()
        self.chart.addSeries(self.series)

        self.x = 0
        self.y = 0

    def comboBox(self):

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

        self.show

    def updateData(self):
        coordinate = observer.get("framePosition")
        self.frameLandmarks = observer.get("faceLandmarks")
        landmarks = self.frameLandmarks[coordinate].landmark
        self.x += 1
        self.y = str((landmarks[61].x-landmarks[78].x)/(landmarks[13].y-landmarks[14].y))
        self.series.append(self.x, self.y)
    # def onActivated(self):

    # def paintEvent(self, event):
    #     painter = QtGui.QPainter(self)
    #     painter.fillRect(self.rect(), QtGui.QColor("white"))