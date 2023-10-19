import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QLine
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QWheelEvent
import urllib.request

from_class = uic.loadUiType("paint.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.pixmap = QPixmap(self.label.width(), self.label.height())
        self.pixmap.fill(Qt.white)
        
        self.label.setPixmap(self.pixmap)
        # self.draw()
        self.x, self.y = None, None
    def wheelEvent(self, event):
        self.label_4.setText(f'Mouse Wheel: ({event.angleDelta().x()}, {event.angleDelta().y()})')
        # self.update()

    def mouseMoveEvent(self, event):
        if self.x is None:
            self.x = event.x()
            self.y = event.y()
            return
        
        self.label_2.setText(f'Mouse Point: local ({event.x(), event.y()}), global ({event.globalX()}, {event.globalY()})')
        self.update()
        
        self.x = event.x()
        self.y = event.y()
    
    def mousePressEvent(self, e):
        click = 'Mouse Press: '        
        if e.button() == Qt.LeftButton:
            click = 'Mouse Press: Left'
        if e.button() == Qt.RightButton:
            click = 'Mouse Press: Right'
        self.label_3.setText(click)
        self.update()
        
    
    def draw(self):
        # painter = QPainter(self.label.pixmap())
        
        # self.pen = QPen(Qt.red, 5, Qt.SolidLine)
        # painter.setPen(self.pen)
        
        # painter.drawLine(100, 100, 500, 100)
        
        # self.pen.setBrush(Qt.blue)
        # self.pen.setWidth(10)
        # self.pen.setStyle(Qt.DashDotLine)
        # painter.setPen(self.pen)
    
        # self.line = QLine(100, 200, 500, 200)
        # painter.drawLine(self.line)
        
        # painter.setPen(QPen(Qt.black, 20, Qt.DotLine))
        # self.p1 = QPoint(100, 300)
        # self.p2 = QPoint(500, 300)
        # painter.drawLine(self.p1, self.p2)
        # painter.end 
        
        # 커다란 점
        # painter = QPainter(self.label.pixmap())
        # painter.setPen(QPen(Qt.red, 20, Qt.SolidLine))
        # painter.drawPoint(100, 200)
        # painter.end
        
        # 사각형
        painter = QPainter(self.label.pixmap())
        
        # painter.setPen(QPen(Qt.blue, 5, Qt.SolidLine))
        # painter.setBrush(QBrush(Qt.black))
        # painter.drawRect(100, 100, 100, 100)
        # painter.drawEllipse(100, 100, 100, 100)
        
        self.font = QFont()
        self.font.setFamily('Times')
        self.font.setBold(True)
        self.font.setPointSize(20)
        painter.setFont(self.font)
        
        painter.drawText(100, 100, 'This is drawText')
        painter.end

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
    
    