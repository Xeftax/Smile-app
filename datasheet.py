import observer
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox

class DataSheetWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Data Sheet")
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Index','Distance'])
        self.tableWidget.setColumnWidth(0,165)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Distance")
        self.comboBox.addItem("Speed")

        self.layout = QVBoxLayout(self, contentsMargins=QtCore.QMargins(0,0,0,0))
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.tableWidget)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        

        # self.data = [[None]*8]
        self.data = [[] for _ in range(8)]
        observer.update("distanceDatas",self.data)

        observer.register("framePosition",self.updateTable)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Lip Length"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Upper Lip Thickness"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Lower Lip Thickness"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Interlabial Gap"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(4, 0, QTableWidgetItem("Commissure Corridor Left"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(5, 0, QTableWidgetItem("Commissure Corridor Right"))
        self.tableWidget.setItem(5, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(6, 0, QTableWidgetItem("Smile Width"))
        self.tableWidget.setItem(6, 1, QTableWidgetItem(None))
        self.tableWidget.setItem(7, 0, QTableWidgetItem("Smile Index"))
        self.tableWidget.setItem(7, 1, QTableWidgetItem(None))


    def updateTable(self, framePosition):

        coordinate = observer.get("framePosition")

        self.frameLandmarks = observer.get("faceLandmarks")

        if self.frameLandmarks and coordinate < len(self.frameLandmarks):

            landmarks = self.frameLandmarks[coordinate]
            
            self.data[0].append(landmarks[0][1]-landmarks[2][1])
            self.data[1].append(landmarks[13][1]-landmarks[0][1])
            self.data[2].append(landmarks[17][1]-landmarks[14][1])
            self.data[3].append(landmarks[14][1]-landmarks[13][1])
            self.data[4].append(landmarks[78][0]-landmarks[61][0])
            self.data[5].append(landmarks[388][0]-landmarks[291][0])
            self.data[6].append(landmarks[291][0]-landmarks[61][0])
            self.data[7].append((landmarks[61][0]-landmarks[78][0])/(landmarks[13][1]-landmarks[14][1]))

            self.tableWidget.setItem(0, 1, QTableWidgetItem("{:.2f}".format(self.data[0][-1])))
            self.tableWidget.setItem(1, 1, QTableWidgetItem("{:.2f}".format(self.data[1][-1])))
            self.tableWidget.setItem(2, 1, QTableWidgetItem("{:.2f}".format(self.data[2][-1])))
            self.tableWidget.setItem(3, 1, QTableWidgetItem("{:.2f}".format(self.data[3][-1])))
            self.tableWidget.setItem(4, 1, QTableWidgetItem("{:.2f}".format(self.data[4][-1])))
            self.tableWidget.setItem(5, 1, QTableWidgetItem("{:.2f}".format(self.data[5][-1])))
            self.tableWidget.setItem(6, 1, QTableWidgetItem("{:.2f}".format(self.data[6][-1])))
            self.tableWidget.setItem(7, 1, QTableWidgetItem("{:.2f}".format(self.data[7][-1])))
            
            
            observer.update("distanceDatas",self.data)

            self.update()
