import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import datetime

from_class = uic.loadUiType("Test7.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.btnAdd.clicked.connect(self.Add)
        
    def Add(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(self.editName.text()))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(self.editGender.text()))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(self.editBirthday.text()))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    
    sys.exit(app.exec_())