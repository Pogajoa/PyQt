import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import datetime

from_class = uic.loadUiType("Test6.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        for year in range(1900, 2023 + 1):
            self.cbYear.addItem(str(year))
        
        for month in range(1, 12 + 1):
            self.cbMonth.addItem(str(month))
        
        for day in range(1, 31 + 1):
            self.cbDay.addItem(str(day))
            
        #self.cbYear.setCurrentText(str(1990))
        self.cbDay.currentIndexChanged.connect(self.printBirthday)
        self.calendarWidget.clicked.connect(self.selectDate)
        
    def selectDate(self):
        date = self.calendarWidget.selectedDate()
        year = date.toString('yyyy')
        month = date.toString('M')
        day = date.toString('d')
        
        self.cbYear.setCurrentText(year)
        self.cbMonth.setCurrentText(month)
        self.cbDay.setCurrentText(day)
        self.lineEdit.setText(year + month.zfill(2) + day.zfill(2))

    def printBirthday(self):
        year = int(self.cbYear.currentText())
        month = int(self.cbMonth.currentText())
        day = int(self.cbDay.currentText())
        birthday = datetime.date(year, month, day).strftime("%Y년-%m월-%d일")
        # self.lineEdit.setText(year + month.zfill(2) + day.zfill(2))
        self.lineEdit.setText(birthday)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    
    sys.exit(app.exec_())