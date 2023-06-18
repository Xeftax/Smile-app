import sys
import math
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QApplication, QVBoxLayout, QMainWindow, QSizePolicy
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QTimer

import datasheet
import observer

class CurvesWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Curves")

        # ComboBox for the parameters
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Lip Lenth")
        self.comboBox.addItem("Upper Lip Thickness")
        self.comboBox.addItem("Lower Lip Thickness")
        self.comboBox.addItem("Interlabial Gap")
        self.comboBox.addItem("Commissure Corridor Left")
        self.comboBox.addItem("Commissure Corridor Right")
        self.comboBox.addItem("Smile Width")
        self.comboBox.addItem("Smile Index")

        # Connect signals to the methods
        self.comboBox.currentTextChanged.connect(self.onComboBoxTextChanged)

        # Graph set up
        self.chart = QChart()
        self.chartView = QChartView(self.chart)
        self.chartView.setChart(self.chart)
        # self.chartView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.chartView.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        # self.chartView.setVisible(True)

        self.pointLineSeries = QLineSeries()
        self.chart.addSeries(self.pointLineSeries)

        self.axisX = QValueAxis()
        self.axisX.setRange(0,60)
        self.chart.addAxis(self.axisX,QtCore.Qt.AlignBottom)
        self.pointLineSeries.attachAxis(self.axisX)

        axisY = QValueAxis()
        axisY.setRange(0,0.3)
        self.chart.addAxis(axisY,QtCore.Qt.AlignLeft)
        self.pointLineSeries.attachAxis(axisY)

        self.x = list(range(60))
        self.y = [0] * len(self.x)
        self.comboBoxChoice = 0
        self.indexChoice = 0
        
        # self.show() 

        layout = QVBoxLayout(self, contentsMargins=QtCore.QMargins(0,0,0,0))
        layout.addWidget(self.comboBox)
        layout.addWidget(self.chartView)
               
        observer.register("framePosition",self.updatePlotData)
      

    def onComboBoxTextChanged(self, text):

        coordinate = observer.get("framePosition")
        self.frameLandmarks = observer.get("faceLandmarks")
        landmarks = self.frameLandmarks[coordinate].landmark

        if text == "Lip Lenth":
            self.comboBoxChoice = landmarks[0].y-landmarks[2].y
            self.indexChoice = 0
        elif text == "Upper Lip Thickness":
            self.comboBoxChoice = landmarks[13].y-landmarks[0].y
            self.indexChoice = 1
        elif text == "Lower Lip Thickness":
            self.comboBoxChoice = landmarks[17].y-landmarks[14].y
            self.indexChoice = 2
        elif text == "Interlabial Gap":
            self.comboBoxChoice = landmarks[14].y-landmarks[13].y
            self.indexChoice = 3
        elif text == "Commissure Corridor Left":
            self.comboBoxChoice = landmarks[78].x-landmarks[61].x
            self.indexChoice = 4
        elif text == "Commissure Corridor Right":
            self.comboBoxChoice = landmarks[388].x-landmarks[291].x
            self.indexChoice = 5
        elif text == "Smile Width":
            self.comboBoxChoice = landmarks[291].x-landmarks[61].x
            self.indexChoice = 6
        elif text == "Smile Index":
            self.comboBoxChoice = (landmarks[61].x-landmarks[78].x)/(landmarks[13].y-landmarks[14].y)
            self.indexChoice = 7
             
    

    def updatePlotData(self, framePosition): 
        data = observer.get("distanceDatas")
        self.y = data[self.indexChoice][-1]
        self.x = len(data[self.indexChoice])-1
        if self.x > 60:
            self.axisX.setRange(self.x-60,self.x)
        self.pointLineSeries.append(self.x,self.y)


