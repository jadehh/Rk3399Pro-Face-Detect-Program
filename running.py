import sys, cv2, time,os
import subprocess
from main_ui import Ui_TabWidget

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog,QTabWidget

from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt

from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QLabel,QWidget
import datetime
from detect_face import *


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
        th = captuerThread(self)
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
            p = image.scaled(84, 84, Qt.IgnoreAspectRatio)
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





class captuerThread(QThread):#采用线程来播放视频
    changePixmap = pyqtSignal(QtGui.QImage)
    changePicturePixmap = pyqtSignal(QtGui.QImage)
    changeDetecPixmap = pyqtSignal(list)
    def run(self):
        cap = cv2.VideoCapture(cameraID)
        # cap.get(cv2.WINDOW_AUTOSIZE)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
        print("打开摄像头成功")
        index = 0
        while (cap.isOpened()==True):
            ret, frame = cap.read()
            #frame = cv2.imread("image/174.jpg")
            if ret:
                print ("----------start taking picture -----------",index)
                scale = ([frame.shape[0] / 344, frame.shape[1] / 450,
                          frame.shape[0] / 344, frame.shape[1] / 450,1])
                img = cv2.resize(frame,(450,344))
                img_matlab = img.copy()
                img_matlab = cv2.cvtColor(img_matlab,cv2.COLOR_BGR2RGB)
                boundingboxes, points = detect(img_matlab, minsize, pnet_rknn_list, rnet_rknn, onet_rknn, threshold ,factor)
                print("检测完成")
                if boundingboxes.shape[0] > 0:
                    result_img,face_img = drawBoxes(frame, boundingboxes*scale)
                    face_img = cv2.cvtColor(face_img,cv2.COLOR_BGR2BGRA)
                    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2BGRA)
                    convertToQtFaceImg = QtGui.QImage(face_img.data,face_img.shape[1],face_img.shape[0],QImage.Format_RGB32)
                    convertToQtFormat = QtGui.QImage(result_img.data, result_img.shape[1], result_img.shape[0],QImage.Format_RGB32)  # 在这里可以对每帧图像进行处理，
                    self.changePixmap.emit(convertToQtFormat)
                    self.changePicturePixmap.emit(convertToQtFaceImg)
                    self.changeDetecPixmap.emit([convertToQtFormat,convertToQtFaceImg])
                else:
                    result_img = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                    convertToQtFormat = QtGui.QImage(result_img.data, result_img.shape[1], result_img.shape[0],
                                                     QImage.Format_RGB32)  # 在这里可以对每帧图像进行处理，
                    self.changePixmap.emit(convertToQtFormat)

                index = index + 1
            else:
                break



if __name__ == '__main__':

    # 注册5号io
    print("已经创建需要先销毁")
    os.system("sudo sh -c  'echo 5 > /sys/class/gpio/unexport'")
    print("申请控制5号IO")
    os.system("sudo sh -c 'echo 5 > /sys/class/gpio/export'")

    print("申请控制5号IO 为 out")
    os.system("sudo sh -c  'echo out > /sys/class/gpio/gpio5/direction'")

    print("先将电频调节到0")
    os.system("sudo sh -c  'echo 0 > /sys/class/gpio/gpio5/value'")

    minsize, pnet_rknn_list, rnet_rknn, onet_rknn, threshold, factor = load_parms()

    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

