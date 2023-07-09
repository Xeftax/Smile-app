import observer
import numpy as np
import mediapipe as mp
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox

class DataSheetWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Data Sheet")
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Name','Value'])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.MultiSelection)
        self.tableWidget.clicked.connect(self.handle_item_clicked)
        self.tableWidget.selectRow(0)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Distance")
        self.comboBox.addItem("Speed")

        self.layout = QVBoxLayout(self, contentsMargins=QtCore.QMargins(0,0,0,0))
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.tableWidget)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.data = {'Lip Length' : [(0,2),[],'#59adf6'],
                    'Upper Lip Thickness' : [(13,0),[],'#42d6a4'],
                    'Lower Lip Thickness' : [(17,14),[],'#ffb480'],
                    'Interlabial Gap' : [(14,13),[],'#c780e8'],
                    'Commissure Corridor Left' : [(78,61),[],'#08cad1'],
                    'Commissure Corridor Right' : [(388,291),[],'#f8f38d'],
                    'Smile Width' : [(291,61),[],'#ff6961'],
                    'Smile Index' : [('Commissure Corridor Left','Interlabial Gap'),[],'#9d94ff']}
        
        self.selectedSegment = [list(self.data.keys())[0]]

        observer.update("computedData",self.data)
        observer.update("selectedSegment",self.selectedSegment)
        observerIndex = observer.register("framePosition",self.updateTable) 
        observer.register("isRecording",lambda value, self=self: observer.unregister("framePosition",observerIndex) if value else setattr(self,"observerIndex",observer.register("framePosition",self.updateTable)))             
        observer.register("faceLandmarks",self.computeData)

        for i,segment in enumerate(self.data):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(segment))


    def updateTable(self, framePosition):
        for i,segment in enumerate(self.data):
            if len(self.data[segment][1]) > framePosition and isinstance(self.data[segment][1][framePosition],float):
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(round(self.data[segment][1][framePosition],1))))
            else:
                self.tableWidget.setItem(i, 1, QTableWidgetItem('Error'))

        self.update()


    def computeData(self, landmarks):
        for segment in self.data:
            self.data[segment][1] = []
        for frame_landmarks in landmarks:
            for segment in self.data:
                value = None
                if frame_landmarks: 
                    if isinstance(self.data[segment][0][0],int):
                        x1,y1 = frame_landmarks[self.data[segment][0][0]][:2]
                        x2,y2 = frame_landmarks[self.data[segment][0][1]][:2]
                        if None not in [x1,y1,x2,y2]:
                            size = observer.get("imageSize")
                            p1 = mp.solutions.drawing_utils._normalized_to_pixel_coordinates(x1,y1, size[1], size[0])
                            p2 = mp.solutions.drawing_utils._normalized_to_pixel_coordinates(x2,y2, size[1], size[0])
                            if p1 and p2:
                                value = np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
                    elif isinstance(self.data[segment][0][0],str):
                        d1,d2 = self.data[self.data[segment][0][0]][1][-1],self.data[self.data[segment][0][1]][1][-1]
                        value = d1/d2 if None not in [d1,d2] and d2 !=0 else None
                self.data[segment][1].append(value)
        observer.update("computedData",self.data)

    def handle_item_clicked(self, item):
        if self.tableWidget.selectionModel().isSelected(item):
            self.selectedSegment.append(list(self.data.keys())[item.row()])
        else:
            self.selectedSegment.remove(list(self.data.keys())[item.row()])
        observer.update("selectedSegment",self.selectedSegment)

        
