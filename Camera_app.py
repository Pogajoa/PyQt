import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import urllib.request
import cv2, imutils
import datetime
import time   
import numpy as np

from_class = uic.loadUiType("Camera_app.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.isCameraOn = False     
        self.isRecStart = False
        self.drawOnPic = False
        
        self.btnRecord.hide()
        self.btnCapture.hide()
        
        self.pixmap = QPixmap(self.label.width(), self.label.height())
        # self.pixmap.fill(Qt.white)
        
        self.label.setPixmap(self.pixmap)
        self.x, self.y = None, None

        self.camera = Camera(self)
        self.camera.daemon = True
        
        self.record = Camera(self)
        self.record.daemon = True
        
        self.btnOpen.clicked.connect(self.openFile)        
        self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.btnCapture.clicked.connect(self.capture)
        self.btnDraw.clicked.connect(self.clickDraw)
        self.count = 0
        self.selected_color = None
        
        
        self.redSlider.setRange(0, 255)
        self.greenSlider.setRange(0, 255)
        self.blueSlider.setRange(0, 255)

        # self.redSlider.setSingleStep(1)
        # self.greenSlider.setSingleStep(1)
        # self.blueSlider.setSingleStep(1)
        
        self.hueSlider.setRange(0, 360)
        self.saturationSlider.setRange(0, 100)
        self.valueSlider.setRange(0, 100)
        
        self.redSlider.valueChanged.connect(self.update_image)
        self.greenSlider.valueChanged.connect(self.update_image)
        self.blueSlider.valueChanged.connect(self.update_image)
        
        self.hueSlider.valueChanged.connect(self.update_image)
        self.saturationSlider.valueChanged.connect(self.update_image)
        self.valueSlider.valueChanged.connect(self.update_image)
        self.drawColorBtn.clicked.connect(self.selectColor)
        self.clearBtn.clicked.connect(self.clearDrawing)
        self.btnDraw.clicked.connect(self.startDrawing)
        self.saveRectBtn.clicked.connect(self.saveArea)
        self.pixmap_origin = self.pixmap.copy() 
        self.drawing = False
        self.points  = []
        
    def startDrawing(self):
        self.drawing = True
        self.points = []
    
    
    def saveArea(self):
        if self.points:     
            rect = self.getBoundingBox()
            image = self.pixmap_origin.copy(rect)  # 직사각형 영역만 복사
            image.save("drawn_area.png")
        self.label.setPixmap(self.pixmap_origin)


    def getBoundingBox(self):
        if not self.points:
            return QRect()

        x_values = [point.x() for point in self.points]
        y_values = [point.y() for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        return QRect(min_x, min_y, max_x - min_x, max_y - min_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.points.append(event.pos())
            self.updateDrawing()

    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            self.updateDrawing()
            
    
    def mouseMoveEvent(self, event):
        if self.drawing:
            self.points.append(event.pos())
            self.updateDrawing()
            
        # if self.drawOnPic == True:
        #     if self.x is None:
        #         self.x = event.x()
        #         self.y = event.y()
            
        #     painter = QPainter(self.label.pixmap())
            
        #     # Create a QPen with the selected color
        #     if self.selected_color != None:
        #         pen = QPen(self.selected_color)
        #         painter.setPen(pen)
            
        #     painter.drawLine(self.x, self.y, event.x(), event.y())
        #     painter.end()
            
        #     self.update()
            
        #     self.x = event.x()
        #     self.y = event.y()
    
    
    def updateDrawing(self):
        painter = QPainter(self.pixmap)
        painter.drawPixmap(0, 0, self.label.pixmap())

        if len(self.points) > 1:
            pen = QPen()
            pen.setColor(self.selected_color)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawPolyline(QPolygon(self.points))

        self.label.setPixmap(self.pixmap)
    
    def selectColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color 
        
     
    def clearDrawing(self):
        if self.points:
            self.label.setPixmap(self.pixmap_origin)
                   
        
    def update_image(self):
        image = self.pixmap.toImage()
        r, g, b = [self.redSlider.value(), self.greenSlider.value(), self.blueSlider.value()]
        h, s, v = [self.hueSlider.value(), self.saturationSlider.value(), self.valueSlider.value()]
        for y in range(image.height()):
            for x in range(image.width()):
                pixel_color = QColor(image.pixel(x, y))

                # Adjust RGB values
                pixel_color.setRed(min(255, max(0, pixel_color.red() + r)))
                pixel_color.setGreen(min(255, max(0, pixel_color.green() + g)))
                pixel_color.setBlue(min(255, max(0, pixel_color.blue() + b)))

                # Convert to HSV color space
                hsv = pixel_color.getHsv()
                hue = hsv[0]
                saturation = hsv[1]
                value = hsv[2]
                
                hue = (hue + h) % 360
                saturation = min(255, max(0, saturation + s))
                value = min(255, max(0, value + v))
                
                # pixel_color.setRgb(red, green, blue)
                pixel_color.setHsv(hue, saturation, value)
                
                image.setPixelColor(x, y, pixel_color)
        self.label.setPixmap(QPixmap.fromImage(image))

   
    def clickDraw(self):
        if self.drawOnPic == False:
            self.drawOnPic = True  
            self.btnDraw.setText('Stop drawing')
        else:
            self.drawOnPic = False
            self.btnDraw.setText('Draw on picture')

        
    def capture(self):
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.png'
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, self.image)
        
    def updateRecording(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(self.image)

     
    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText('Rec Stop')
            self.isRecStart = True
            
            self.recordingStart()
        else:
            self.btnRecord.setText('Rec Start')
            self.isRecStart = False 
            
            self.recordingStop()
             
    def recordingStart(self):
        self.record.running = True
        self.record.start()
        
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))
                
    def recordingStop(self):
        self.record.running = False
        
        if self.isRecStart == True:  
            self.writer.release()
    
    def updateCamera(self):
        # self.label.setText('Camera Runnning: ' + str(self.count))
        self.count += 1
        
        retval, self.image = self.video.read()
        if retval:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            h, w, c  = self.image.shape   
            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            
            self.image = image

            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
            
            self.label.setPixmap(self.pixmap)

        self.count += 1
        
        
    def clickCamera(self):
        if self.isCameraOn == False:
            self.btnCamera.setText('Camera off')
            self.isCameraOn = True
            self.btnRecord.show()
            self.btnCapture.show()
            
            self.cameraStart()
        else:
            self.btnCamera.setText('Camera on')
            self.isCameraOn = False
            self.btnRecord.hide()
            self.btnCapture.hide()
            
            self.cameraStop()
            self.recordingStop()
    
    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)
    
    def cameraStop(self):
        self.camera.running = False  
        self.camera.count = 0
        self.video.release()
        
        if self.isRecStart == True:
            self.writer.release()
        
            
    def openFile(self):
        file = QFileDialog.getOpenFileName(self, 'Open File', './')
        
        if file[0][-3:] == 'png':
            image = cv2.imread(file[0])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
            h, w, c = image.shape
            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
            
            self.label.setPixmap(self.pixmap)
            self.pixmap_origin = self.pixmap.copy() 

        elif file[0][-3:] == 'avi':
            cap = cv2.VideoCapture(file[0])
            fps = cap.get(cv2.CAP_PROP_FPS)
            sleep_ms = int(np.round((1/fps) * 500))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                
                p = pixmap.scaled(int(w*400/h), 480, QtCore.Qt.IgnoreAspectRatio)
                self.ui.label.setPixmap(p)
                
                if (cv2.waitKey(sleep_ms) == ord('q')):
                    break
            cap.release()
            cv2.destroyAllWindows()

class Camera(QThread):
    update = pyqtSignal()
    def __init__(self, sec = 0, parent = None):
        super().__init__()
        self.main = parent
        self.running = True    
        
    def run(self):
        count = 0  
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)
            
    def stop(self):
        self.running = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())