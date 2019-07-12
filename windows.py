import sys, cv2, time,os
import subprocess
from main_ui import Ui_TabWidget

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog,QTabWidget

from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt

from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QLabel,QWidget
import datetime


windowWidth = 1920
windowHeight = 1080

def GetTime():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d  %H:%M")
    return otherStyleTime
def GetSeconds():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d  %H:%M:%S")
    return otherStyleTime.split(":")[-1]

class mywindow(QtWidgets.QMainWindow,Ui_TabWidget): #这个窗口继承了用QtDesignner 绘制的窗口

    def __init__(self):
        super(mywindow,self).__init__()
        self.picture_index = 0
        self.hiddenWidget = True
        self.setupUi(self)


    def cameraprocessing(self):
        global cameraID
        cameraID = 0
        th = captuerThreadWindows(self)
        th.changePixmap.connect(self.setImage)
        th.changePicturePixmap.connect(self.setPictureImage)
        th.changeDetecPixmap.connect(self.setDetectResultImage)
        th.start()

    def setImage(self, image):
        image = image.scaled(1020, 765, Qt.IgnoreAspectRatio)
        self.imageWidget.imageLabel.setPixmap(QPixmap.fromImage(image))

    def HiddenLabel(self):
        self.imageWidget.setPictureHidden()
        self.hiddenWidget = True


    def InitAnno2(self):
        self.imageWidget.initAnimation2()


    #设置当前检测的图片
    def setDetectResultImage(self,images):
        if self.hiddenWidget == True:
            self.imageWidget.setPictireShow(images)
            timer = QTimer()
            timer.singleShot(3000, self.HiddenLabel)
            timer2 = QTimer()
            timer2.singleShot(500, self.InitAnno2)
            openThread = OpenDoor(self)
            openThread.start()
            self.hiddenWidget = False;





    #设置最右边的历史状态图片
    def setPictureImage(self,image):
        if self.hiddenWidget == True:
            p = image.scaled(windowWidth * 0.12, windowWidth * 0.12, Qt.KeepAspectRatio)
            self.resultWidget.ImageLabelArr[self.picture_index].setPixmap(QPixmap.fromImage(p))
            self.resultWidget.TimeLabelArr[self.picture_index].setText(GetTime())
            self.picture_index = self.picture_index + 1
            if self.picture_index > 6:
                self.picture_index = 0




class OpenDoor(QThread):
    def run(self):
        os.system("sudo sh -c  'echo 1 > /sys/class/gpio/gpio5/value'")
        self.sleep(1)
        os.system("sudo sh -c  'echo 0 > /sys/class/gpio/gpio5/value'")






class captuerThreadWindows(QThread):#采用线程来播放视频
    changePixmap = pyqtSignal(QtGui.QImage)
    changePicturePixmap = pyqtSignal(QtGui.QImage)
    changeDetecPixmap = pyqtSignal(list)
    def run(self):
        print("打开摄像头成功")
        cap = cv2.VideoCapture("sources/192.168.0.113_01_20180823150115648.mp4")
        ret,frame = cap.read()
        index = 0
        while (ret):
            print("----------start taking picture -----------", index)
            img = cv2.resize(frame, (450, 344))
            img_matlab = img.copy()
            img_matlab = cv2.cvtColor(img_matlab, cv2.COLOR_BGR2RGB)
            if index % 10 == 0:
                face_img = img_matlab.copy()
                result_img = img_matlab.copy()
                face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGBA)
                result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGBA)
                convertToQtFaceImg = QtGui.QImage(face_img.data, face_img.shape[1], face_img.shape[0],
                                                  QImage.Format_RGB32)
                convertToQtFormat = QtGui.QImage(result_img.data, result_img.shape[1], result_img.shape[0],
                                                 QImage.Format_RGB32)  # 在这里可以对每帧图像进行处理，
                self.changePixmap.emit(convertToQtFormat)
                self.changePicturePixmap.emit(convertToQtFaceImg)
                self.changeDetecPixmap.emit([convertToQtFaceImg,convertToQtFaceImg])
            else:
                result_img = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                convertToQtFormat = QtGui.QImage(result_img.data, result_img.shape[1], result_img.shape[0],
                                                 QImage.Format_RGB32)  # 在这里可以对每帧图像进行处理，
                self.changePixmap.emit(convertToQtFormat)
            ret, frame = cap.read()
            time.sleep(0.1)
            index = index + 1

if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

