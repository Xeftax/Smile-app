
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QComboBox, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
import observer

class CurvesWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Curves")

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
        layout.addWidget(self.chartView)
               
        observer.register("framePosition",self.updatePlotData)
      

    def onComboBoxTextChanged(self, text):

        coordinate = observer.get("framePosition")
        self.frameLandmarks = observer.get("faceLandmarks")
        landmarks = self.frameLandmarks[coordinate]

        if text == "Lip Lenth":
            self.comboBoxChoice = landmarks[0][1]-landmarks[2][1]
            self.indexChoice = 0
        elif text == "Upper Lip Thickness":
            self.comboBoxChoice = landmarks[13][1]-landmarks[0][1]
            self.indexChoice = 1
        elif text == "Lower Lip Thickness":
            self.comboBoxChoice = landmarks[17][1]-landmarks[14][1]
            self.indexChoice = 2
        elif text == "Interlabial Gap":
            self.comboBoxChoice = landmarks[14][1]-landmarks[13][1]
            self.indexChoice = 3
        elif text == "Commissure Corridor Left":
            self.comboBoxChoice = landmarks[78][0]-landmarks[61][0]
            self.indexChoice = 4
        elif text == "Commissure Corridor Right":
            self.comboBoxChoice = landmarks[388][0]-landmarks[291][0]
            self.indexChoice = 5
        elif text == "Smile Width":
            self.comboBoxChoice = landmarks[291][0]-landmarks[61][0]
            self.indexChoice = 6
        elif text == "Smile Index":
            self.comboBoxChoice = (landmarks[61][0]-landmarks[78][0])/(landmarks[13][1]-landmarks[14][1])
            self.indexChoice = 7
             
    

    def updatePlotData(self, framePosition): 
        data = observer.get("distanceDatas")
        self.y = data[self.indexChoice][-1]
        self.x = len(data[self.indexChoice])-1
        if self.x > 60:
            self.axisX.setRange(self.x-60,self.x)
        self.pointLineSeries.append(self.x,self.y)


