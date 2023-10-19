import mysql.connector
local = mysql.connector.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "1",
    database = "armbase"
)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import datetime

from_class = uic.loadUiType("practice1.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cur = local.cursor()
        
        # Select gender
        self.cur.execute("SELECT DISTINCT SEX from celeb")
        sexes = self.cur.fetchall()
        for sex in sexes:
            sex = str(sex)
            if 'M' in sex:
                sex = 'M'
            elif 'F' in sex:
                sex = 'F'
            self.cbSex.addItem(sex)
        
        # Select JobTitle
        self.cur.execute("SELECT DISTINCT JOB_TITLE from celeb")
        jobs = self.cur.fetchall()
        for job in jobs:
            job = str(job).replace("'", "").replace('(', '').replace(')', '')
            jobs = job.split(',')
            for i in range(len(jobs)):
                jobs[i] = jobs[i].lstrip()
                jobs[i] = jobs[i].rstrip()
            s1 = []
            for job in jobs:
                if job != '' and job not in s1:
                    s1.append(job)
            s1 = set(s1)
            s1 = sorted(s1)
            for job_name in s1:
                print(job_name)
                self.cbJobtitle.addItem(job_name)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    
    sys.exit(app.exec_())
local.close()