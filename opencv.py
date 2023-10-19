import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
# from camera import Camera
import cv2, imutils
import datetime
import time   
import numpy as np

from_class = uic.loadUiType("opencv.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.isCameraOn = False     
        self.isRecStart = False
        self.btnRecord.hide()
        self.btnCapture.hide()
        
        self.pixmap = QPixmap()
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
        
        self.count = 0
    
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
        self.label.setText('Camera Runnning: ' + str(self.count))
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
        self.video.release
        
        if self.isRecStart == True:
            self.writer.release()
        
            
    def openFile(self):
        file = QFileDialog.getOpenFileName(self, 'Open File', './')
        
        if file[0][-3:] == 'png':
            cap = cv2.VideoCapture(file[0])
            fps = cap.get(cv2.CAP_PROP_FPS)
            sleep_ms = int(numpy.round((1, fps) * 500))
            
            while cap.isOpened():    
                # if self.running == False:
                #     break
                ret,frame = cap.read()
                if not ret:
                    break
                
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.Qpixmap.fromImage(qImg)
            
                p = pixmap.scaled(int(w*480/h), 480, QtCore.Qt.IgnoreAspectRatio)
                self.ui.label.setPixmap(p)
                
                if (cv2.waitKey(sleep_ms) == ord('q')):
                    break
                
            # cap.release()
            # cv2.destroyAllWindows()
            
            
            # h, w, c = image.shape
            # qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            
            # self.image = image

            # self.pixmap = self.pixmap.fromImage(qimage)
            # self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
            
            # self.label.setPixmap(self.pixmap)

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