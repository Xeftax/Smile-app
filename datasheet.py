import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QHeaderView, QTableView, QTableWidget, QTableWidgetItem

class DataSheetWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("Data Sheet")
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(7)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Lip Length"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("y[2]-y[0]"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Upper Lip Thickness"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("y[0]-y[13]"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Lower Lip Thickness"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("y[14]-y[17]"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Interlabial Gap"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("y[13]-y[14]"))
        self.tableWidget.setItem(4, 0, QTableWidgetItem("Commissure Corridor Left"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem("x[61]-x[78]"))
        self.tableWidget.setItem(5, 0, QTableWidgetItem("Commissure Corridor Right"))
        self.tableWidget.setItem(5, 1, QTableWidgetItem("x[308]-x[291]"))
        self.tableWidget.setItem(6, 0, QTableWidgetItem("Smile Width"))
        self.tableWidget.setItem(6, 1, QTableWidgetItem("x[61]-x[291]"))
        self.tableWidget.setItem(7, 0, QTableWidgetItem("Smile Index"))
        self.tableWidget.setItem(7, 1, QTableWidgetItem("(x[61]-x[78])/(y[13]-y[14])"))



    # def paintEvent(self, event):
    #     painter = QtGui.QPainter(self)
    #     painter.fillRect(self.rect(), QtGui.QColor("white"))

    # def updateTable(self, data):
    #     self.tableWidget.setRowCount(len(data))

        # for row, item in enumerate(data):
        #     for column, value in enumerate(item):
        #         table_item = QTableWidgetItem(str(value))
        #         self.tableWidget.setItem(row, column, table_item)    