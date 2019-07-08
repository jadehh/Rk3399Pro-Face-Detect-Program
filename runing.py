import sys, cv2, time

from main_ui import Ui_TabWidget

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog,QTabWidget

from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt

from PyQt5.QtGui import QPixmap, QImage

from PyQt5.QtWidgets import QLabel,QWidget
from ArrayQueue import ArrayQueue
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
        self.tempImage = QImage()
        self.setupUi(self)

        self.FirstAnimation = False

    def cameraprocessing(self):
        global cameraID
        cameraID = 0
        th = captuerThread(self)
        th.changePixmap.connect(self.setImage)
        th.changePicturePixmap.connect(self.setPictureImage)
        th.changeDetecPixmap.connect(self.setDetectResultImage)
        th.start()

        self.FirstAnimation = True
    def setImage(self, image):
        self.imageWidget.imageLabel.setPixmap(QPixmap.fromImage(image))

    def HiddenLabel(self):
        print("需要隐藏"+GetSeconds())
        self.imageWidget.setPictureHidden()
        self.hiddenWidget = True
        print("控件已经隐藏起来了")


    def InitAnno2(self):
        print("开启第二次动画")
        self.FirstAnimation = False
        self.imageWidget.initAnimation2(self.tempImage)


    #设置当前检测的图片
    def setDetectResultImage(self,image):
        if self.hiddenWidget == True:
            print("检测到有人脸")
            timer = QTimer()
            timer.singleShot(3000, self.HiddenLabel)
            timer2 = QTimer()
            timer2.singleShot(500, self.InitAnno2)
            self.hiddenWidget = False;
            self.tempImage = image
            self.imageWidget.setPictireShow(image)
            self.imageWidget.imageTemp = QPixmap.fromImage(image)
            self.imageWidget.update()




    #设置最右边的历史状态图片
    def setPictureImage(self,image):
        if self.hiddenWidget == True:
            p = image.scaled(windowWidth * 0.12, windowWidth * 0.12, Qt.KeepAspectRatio)
            self.ImageLabelArr[self.picture_index].userfacePixmap = QPixmap.fromImage(p)
            self.ImageLabelArr[self.picture_index].update()
            self.ImageLabelArr[self.picture_index].savetimeLabel.setText(GetTime())
            self.picture_index = self.picture_index + 1
            if self.picture_index > 6:
                self.picture_index = 0







class captuerThread(QThread):#采用线程来播放视频
    changePixmap = pyqtSignal(QtGui.QImage)
    changePicturePixmap = pyqtSignal(QtGui.QImage)
    changeDetecPixmap = pyqtSignal(QtGui.QImage)
    def run(self):
        cap = cv2.VideoCapture("sources/192.168.0.113_01_20180823150115648.mp4")
        # cap = cv2.VideoCapture(cameraID)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        print("打开摄像头成功")
        index = 0
        while (cap.isOpened()==True):
            ret, frame = cap.read()
            if ret:
                img = cv2.resize(frame,(450,344))
                img_matlab = img.copy()
                # check rgb position
                boundingboxes, points = detect_face(img_matlab, minsize, pnet_rknn_list, rnet_rknn, onet_rknn, threshold, False,
                                        factor)
                if boundingboxes.shape[0] > 0:
                    result_img = drawBoxes(img, boundingboxes)
                    scale = ([frame.shape[0] / 344, frame.shape[1] / 450,
                              frame.shape[0] / 344, frame.shape[1]] / 450)
                    result_img = drawBoxes(frame, boundingboxes * scale)
                    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2BGRA)
                    convertToQtFormat = QtGui.QImage(result_img.data, result_img.shape[1], result_img.shape[0],
                                                     QImage.Format_RGB32)  # 在这里可以对每帧图像进行处理，
                    p = convertToQtFormat.scaled(windowWidth * 0.8, windowHeight * 0.8, Qt.KeepAspectRatioByExpanding)
                    self.changePixmap.emit(p)
                    self.changePicturePixmap.emit(p)
                    self.changeDetecPixmap.emit(p)
            else:
                result_img = img_matlab.copy()
                convertToQtFormat = QtGui.QImage(result_img.data, result_img.shape[1], result_img.shape[0],
                                                 QImage.Format_RGB32)  # 在这里可以对每帧图像进行处理，
                p = convertToQtFormat.scaled(windowWidth * 0.8, windowHeight * 0.8, Qt.KeepAspectRatioByExpanding)
                self.changePixmap.emit(p)
                break




if __name__ == '__main__':
    # print(GetTime())
    minsize = 20
    threshold = [0.6, 0.7, 0.7]
    factor = 0.709
    pnet_rknn_list=init_pnet()
    rnet_rknn = RKNN()
    onet_rknn = RKNN()
    rnet_rknn.load_rknn('./RNet.rknn')
    onet_rknn.load_rknn('./ONet.rknn')
    ret = rnet_rknn.init_runtime()
    if ret != 0:
        print('Init rnet runtime environment failed')
        exit(ret)
    ret = onet_rknn.init_runtime()
    if ret != 0:
        print('Init onet runtime environment failed')
        exit(ret)
    #error = []
    #f = open(imglistfile, 'r')
    sys.stdout = open('/dev/stdout', 'w')
    sys.stderr = open('/dev/stderr', 'w')
    # print("参数初始化成功")
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
