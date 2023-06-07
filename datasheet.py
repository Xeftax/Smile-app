import sys
import observer
import camera
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QHeaderView, QTableView, QTableWidget, QTableWidgetItem

class DataSheetWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Data Sheet")
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Index','Distance'])
        self.tableWidget.setColumnWidth(0,160)

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



    # def paintEvent(self, event):
    #     frameLandmarks = observer.get("frameLandmarks")

    def updateTable(self, framePosition):

        # self.frameLandmarks = observer.get("frameLandmarks")[framePosition]

        # self.tableWidget.setItem(0, 1, QTableWidgetItem(self.frameLandmarks.landmark[2].y-self.frameLandmarks.landmark[0].y))
        # self.tableWidget.setItem(1, 1, QTableWidgetItem(self.frameLandmarks.landmark[0].y-self.frameLandmarks.landmark[13].y))
        # self.tableWidget.setItem(2, 1, QTableWidgetItem(self.frameLandmarks.landmark[14].y-self.frameLandmarks.landmark[17].y))
        # self.tableWidget.setItem(3, 1, QTableWidgetItem(self.frameLandmarks.landmark[13].y-self.frameLandmarks.landmark[14].y))
        # self.tableWidget.setItem(4, 1, QTableWidgetItem(self.frameLandmarks.landmark[61].x-self.frameLandmarks.landmark[78].x))
        # self.tableWidget.setItem(5, 1, QTableWidgetItem(self.frameLandmarks.landmark[388].x-self.frameLandmarks.landmark[291].x))
        # self.tableWidget.setItem(6, 1, QTableWidgetItem(self.frameLandmarks.landmark[61].x-self.frameLandmarks.landmark[291].x))
        # self.tableWidget.setItem(7, 1, QTableWidgetItem((self.frameLandmarks.landmark[61].x-self.frameLandmarks.landmark[78].x)/(self.frameLandmarks.landmark[13].y-self.frameLandmarks.landmark[14].y)))
            
        # self.update()

        coordinate = observer.get("framePosition")

        self.frameLandmarks = observer.get("faceLandmarks")

        if self.frameLandmarks and coordinate < len(self.frameLandmarks):
            landmarks = self.frameLandmarks[coordinate].landmark
            # print(landmarks[2].y-landmarks[0].y)
            self.tableWidget.setItem(0, 1, QTableWidgetItem(str(landmarks[2].y-landmarks[0].y)))
            self.tableWidget.setItem(1, 1, QTableWidgetItem(str(landmarks[0].y-landmarks[13].y)))
            self.tableWidget.setItem(2, 1, QTableWidgetItem(str(landmarks[14].y-landmarks[17].y)))
            self.tableWidget.setItem(3, 1, QTableWidgetItem(str(landmarks[13].y-landmarks[14].y)))
            self.tableWidget.setItem(4, 1, QTableWidgetItem(str(landmarks[61].x-landmarks[78].x)))
            self.tableWidget.setItem(5, 1, QTableWidgetItem(str(landmarks[388].x-landmarks[291].x)))
            self.tableWidget.setItem(6, 1, QTableWidgetItem(str(landmarks[61].x-landmarks[291].x)))
            self.tableWidget.setItem(7, 1, QTableWidgetItem(str((landmarks[61].x-landmarks[78].x)/(landmarks[13].y-landmarks[14].y))))
            
            self.update()

        # print(coordinate, self.frameLandmarks)

        # if isinstance(coordinate, (str, list, tuple, bytearray, dict, set)):
            
        #     self.frameLandmarks = coordinate

        #     self.tableWidget.setItem(0, 1, QTableWidgetItem(self.frameLandmarks.landmark[2].y-self.frameLandmarks.landmark[0].y))
        #     self.tableWidget.setItem(1, 1, QTableWidgetItem(self.frameLandmarks.landmark[0].y-self.frameLandmarks.landmark[13].y))
        #     self.tableWidget.setItem(2, 1, QTableWidgetItem(self.frameLandmarks.landmark[14].y-self.frameLandmarks.landmark[17].y))
        #     self.tableWidget.setItem(3, 1, QTableWidgetItem(self.frameLandmarks.landmark[13].y-self.frameLandmarks.landmark[14].y))
        #     self.tableWidget.setItem(4, 1, QTableWidgetItem(self.frameLandmarks.landmark[61].x-self.frameLandmarks.landmark[78].x))
        #     self.tableWidget.setItem(5, 1, QTableWidgetItem(self.frameLandmarks.landmark[388].x-self.frameLandmarks.landmark[291].x))
        #     self.tableWidget.setItem(6, 1, QTableWidgetItem(self.frameLandmarks.landmark[61].x-self.frameLandmarks.landmark[291].x))
        #     self.tableWidget.setItem(7, 1, QTableWidgetItem((self.frameLandmarks.landmark[61].x-self.frameLandmarks.landmark[78].x)/(self.frameLandmarks.landmark[13].y-self.frameLandmarks.landmark[14].y)))
            
        #     self.update()

        # else:
        #     print("Error : Pb of subscriptable")


        
        

    # def updateTable(self, data):
    #     self.tableWidget.setRowCount(len(data))

        # for row, item in enumerate(data):
        #     for column, value in enumerate(item):
        #         table_item = QTableWidgetItem(str(value))
        #         self.tableWidget.setItem(row, column, table_item)    