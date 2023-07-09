import time
from PySide6.QtWidgets import QWidget,QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt, QMargins
import observer

class CurvesWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Graph set up
        self.chart = QChart()
        self.chartView = QChartView(self.chart)
        self.chartView.setChart(self.chart)
        #self.chartView.clicked.connect(self.chart_clicked)

        self.pointLineSeries = {}
        self.pointLineRanges = {}
        self.playerLine = QLineSeries()

        self.X = []
        self.xRange = 2
        self.initTime = time.time()
        self.yAxisRange = [float('inf'),0]

        self.chart.legend().hide()
        self.axisX = QValueAxis()
        self.axisX.setRange(0,self.xRange)
        self.chart.addAxis(self.axisX,Qt.AlignBottom)
        self.axisY = QValueAxis()
        self.chart.addAxis(self.axisY,Qt.AlignLeft)

        self.chart.mousePressEvent = self.chart_clicked

        layout = QVBoxLayout(self, contentsMargins=QMargins(0,0,0,0))
        layout.addWidget(self.chartView)
               
        observerIndex = observer.register("framePosition",lambda _: self.updatePlotLiveData()) 
        observer.register("isRecording",lambda value: observer.unregister("framePosition",observerIndex) if value else None)
        observer.register("videoLoaded",lambda value: self.updatePlotRecordData(observer.get("computedData")) if value else None)  

       #observer.register("videoLoaded",lambda value: observer.register("computedData",self.updatePlotRecordData) if value else None)  
    
    def updatePlotRecordData(self,data):
        self.pointLineSeries = {}
        self.chart.removeAllSeries()
        frame_interval = observer.get("loadedFrames")[1]

        self.X = [frame_interval[0]/1000]
        for i in range(len(frame_interval)-1):
            self.X.append(self.X[i]+frame_interval[i+1]/1000)

        for segment in data:
            if segment not in self.pointLineSeries: self.pointLineSeries[segment] = []
            self.createQLineSeries(segment,data[segment][2])
            Y = data[segment][1]
            yRange = [float('inf'),0]
            for x,y in zip(self.X,Y):
                if y: 
                    self.pointLineSeries[segment][-1].append(x,y)
                    yRange = [min(yRange[0],y),max(yRange[1],y)]
                elif self.pointLineSeries[segment][-1].count() > 0: 
                    self.createQLineSeries(segment,data[segment][2])
            self.pointLineRanges[segment] = yRange

        self.axisX.setRange(self.X[0],self.X[-1])

        self.playerLine = QLineSeries()
        self.playerLine.append(0,0)
        self.playerLine.append(0,0)
        self.chart.addSeries(self.playerLine)
        self.playerLine.attachAxis(self.axisX)
        self.playerLine.attachAxis(self.axisY)
        pen = QPen('#999999')
        pen.setWidth(1)
        self.playerLine.setPen(pen)
        observer.register("framePosition",self.updatePlayerPosition)

        self.updateVisibility(observer.get("selectedSegment"))
        observer.register("selectedSegment", self.updateVisibility)

    def updateVisibility(self,selectedSegment):
        yRange = [float('inf'),0]
        for segment in self.pointLineSeries:
            for pointLineSeries in self.pointLineSeries[segment]:
                isVisible = segment in selectedSegment
                pointLineSeries.setVisible(isVisible)
                if isVisible:
                    minY,maxY = self.pointLineRanges[segment]
                    yRange = [min(yRange[0],minY),max(yRange[1],maxY)]
        
        margin = (yRange[1]-yRange[0])*0.1
        ymin,ymax = yRange[0]-margin,yRange[1]+margin
        self.axisY.setRange(ymin,ymax)
        playerX1,playerX2 = self.playerLine.at(0).x(),self.playerLine.at(1).x()
        self.playerLine.replace(0,playerX1,ymin)
        self.playerLine.replace(1,playerX2,ymax)
        
    def updatePlayerPosition(self,position):
        y1,y2 = self.playerLine.at(0).y(),self.playerLine.at(1).y()
        self.playerLine.replace(0,self.X[position],y1)
        self.playerLine.replace(1,self.X[position],y2)
        

    def updatePlotLiveData(self):
        data = observer.get("computedData")
        selectedSegment = observer.get("selectedSegment")

        for segment in selectedSegment:
            if len(data[segment][1]) == 0: continue
            y = data[segment][1][0]
            x = (time.time() - self.initTime)

            margin = (self.yAxisRange[1]-self.yAxisRange[0])*0.1
            self.axisY.setRange(self.yAxisRange[0]-margin,self.yAxisRange[1]+margin)
            self.axisX.setRange(x-self.xRange,x)

            if segment not in self.pointLineSeries: self.pointLineSeries[segment] = []
            if len(self.pointLineSeries[segment]) == 0 or (not y and self.pointLineSeries[segment][-1].count() > 0): 
                self.createQLineSeries(segment,data[segment][2])
            
            if y: 
                lastPointLineSeries = self.pointLineSeries[segment][-1]
                lastPointLineSeries.append(x,y)
                self.yAxisRange = [min([y,self.yAxisRange[0]]),max([y,self.yAxisRange[1]])]
                if lastPointLineSeries.at(0).x() < x-self.xRange:
                    lastPointLineSeries.remove(0)

            for series in reversed(self.pointLineSeries[segment][:-1]):
                seriesLength = series.count()
                if seriesLength == 0 or series.at(seriesLength-1).x() < x-self.xRange:
                    self.chart.removeSeries(series)
                    self.pointLineSeries[segment].remove(series)
            
        for segment in self.pointLineSeries:
            if segment not in selectedSegment and len(self.pointLineSeries[segment]) > 0:
                [self.chart.removeSeries(pointLineSeries) for pointLineSeries in self.pointLineSeries[segment]]
                self.pointLineSeries[segment] = []
                self.yAxisRange = [float('inf'),0]  

    def createQLineSeries(self,segment,color):
        pointLineSeries = QLineSeries()
        self.chart.addSeries(pointLineSeries)
        pointLineSeries.attachAxis(self.axisX)
        pointLineSeries.attachAxis(self.axisY)
        pointLineSeries.setColor(color)
        pointLineSeries.clicked.connect(lambda point: observer.update("goToFrame",self.closerX_index(point.x())) if observer.get("videoLoaded") else None)
        self.pointLineSeries[segment].append(pointLineSeries)

    def closerX_index(self,x):
        a,b = 0,len(self.X)-1
        while b-a > 1:
            m = (a+b)//2
            if self.X[m] < x: a = m
            else: b = m
        return a if x-self.X[a] < self.X[b]-x else b

    def chart_clicked(self, event):
        if len(self.X) != 0 and event.button() == Qt.LeftButton:
            position = self.mapToParent(event.pos())
            x_coord = self.chart.mapToValue(position).x()
            observer.update("goToFrame",self.closerX_index(x_coord))

            


