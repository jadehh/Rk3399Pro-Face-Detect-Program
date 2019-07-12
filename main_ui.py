from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from customizeWidget import ImageWidget,ResultWidget
import datetime


def getWindowSize():
    desktopWidget = QApplication.desktop()
    screenRect = desktopWidget.screenGeometry()
    screenW = screenRect.width()
    screenH = screenRect.height()
    return (1920,1080)



class Ui_TabWidget(object):
    def setupUi(self,Widget):
        widgetW, widgetH = getWindowSize()
        textFont = QFont("Microsoft YaHei",55)

        backgroundLabel = QLabel("",self)
        backgroundLabel.setGeometry(100,0,1420,1080)
        pixmap = QPixmap("sources/bg.png")
        pixmap.scaled(1420,1080, Qt.IgnoreAspectRatio)
        backgroundLabel.setPixmap(pixmap)

        backgroundLabel2 = QLabel("",self)
        backgroundLabel2.setGeometry(0,0,1420,1080)
        pixmap2 = QPixmap("sources/bg.png")
        pixmap2.scaled(100,1080, Qt.IgnoreAspectRatio)
        backgroundLabel2.setPixmap(pixmap2)



        logoLabel = QLabel("",self)
        logoLabel.move(100,98)
        logoLabel.setFixedWidth(312)
        logoLabel.setFixedHeight(64)
        logoPixmap = QPixmap()
        logoPixmap.load("sources/logo.png")
        logoLabel.setPixmap(logoPixmap)



        self.setCacheImage()
        self.timeLabel = QLabel("", self)
        self.timeLabel.setGeometry(1680,90,184,70)
        self.timeLabel.setFont(textFont)
        self.timeLabel.setStyleSheet("color:#A38C62;")
        self.timeLabel.setAlignment(Qt.AlignCenter)



        self.dayLabel = QLabel("", self)
        self.dayLabel.setGeometry(1500,126,180,40)
        self.dayLabel.setStyleSheet("color:#A38C62;")
        self.dayLabel.setFont(QFont("Microsoft YaHei",15))
        self.dayLabel.setAlignment(Qt.AlignRight)
        # 动态显示时间在label上
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()


        self.imageWidget = ImageWidget(self)
        self.imageWidget.setGeometry(100,215,1420,765)





        self.setGeometry(0, 0, widgetW*1, widgetH*1)

        self.setWindowTitle('人脸检测窗口')
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # self.setWindowFlags(Qt::WindowCloseButtonHint | Qt::MSWindowsFixedSizeDialogHint)
        self.show()
        Widget.cameraprocessing()


    def setCacheImage(self):
        widgetW, widgetH = getWindowSize()
        self.resultWidget = ResultWidget(self)
        self.resultWidget.setGeometry(1420,0, 540, 1080)



    def showtime(self):
        dayString,timeString = self.GetTime()
        self.timeLabel.setText(timeString)
        self.dayLabel.setText(dayString)



    def GetTime(self):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d  %H:%M")
        dayString = otherStyleTime.split(" ")[0]
        timeString = otherStyleTime.split(" ")[2]
        return dayString,timeString


