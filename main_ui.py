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

        pal =QtGui.QPalette(self.palette())
        pal.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap("sources/bg.png")))
        self.setPalette(pal)

        logoLabel = QLabel("",self)
        logoLabel.move(100,98)
        logoLabel.setFixedWidth(312)
        logoLabel.setFixedHeight(64)
        logoPixmap = QPixmap()
        logoPixmap.load("sources/logo.png")
        logoLabel.setPixmap(logoPixmap)


        Widget.cameraprocessing()

        self.timeLabel = QLabel("", self)
        self.timeLabel.setGeometry(1647,99,174,56)
        self.timeLabel.setFont(textFont)
        self.timeLabel.setStyleSheet("color:#A38C62;")
        self.timeLabel.setAlignment(Qt.AlignCenter)

        self.dayLabel = QLabel("", self)
        self.dayLabel.setGeometry(1500,136,131,17)
        self.dayLabel.setStyleSheet("color:#A38C62;")
        self.dayLabel.setFont(QFont("Microsoft YaHei",15))
        self.dayLabel.setAlignment(Qt.AlignRight)
        # 动态显示时间在label上
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()


        self.imageWidget = ImageWidget(self)
        self.imageWidget.setGeometry(100,215,1420,765)




        self.setCacheImage()
        self.setGeometry(0, 0, widgetW*1, widgetH*1)

        self.setWindowTitle('人脸检测窗口')
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        # self.setWindowFlags(Qt::WindowCloseButtonHint | Qt::MSWindowsFixedSizeDialogHint)
        self.show()



    def setCacheImage(self):
        widgetW, widgetH = getWindowSize()
        self.ImageLabelArr = []
        for i in range(7):
            self.resultWidget = ResultWidget(self)
            self.resultWidget.setGeometry(1555, 212+105*i, 345, 84)
            self.ImageLabelArr.append(self.resultWidget)

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


