from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QRect,QTimer,QPropertyAnimation,QSize


class ImageWidget(QWidget):
   def __init__(self, parent=None):
       super(ImageWidget, self).__init__(parent)
       self.detecFaceResult = False
       self.startAnnotation1 = False
       self.startAnnotation2 = False

       self.imageLabel = QLabel("", self)
       self.imageLabel.setGeometry(0, 0, 1020, 765)  # 一定要有个东西把它撑起来！！不然看不到
       self.imageLabel.setPixmap(QPixmap("sources/picture_test.jpg"))

       self.op = QGraphicsOpacityEffect()
       self.op.setOpacity(0.5)

       self.pictureWidget = PictureWidget(self)
       self.pictureWidget.setGeometry(300,135,594,454)

       self.afterWidget = AfterDetectWidget(self)
       self.afterWidget.setGeometry(1020,0,400,765)



   def setPictureHidden(self):
       self.op.setOpacity(1)
       self.imageLabel.setGraphicsEffect(self.op)
       self.pictureWidget.setHidden(True)
       self.pictureWidget.setHidden(True)


   def setPictireShow(self,images):
       self.pictureWidget.setHidden(False)
       self.op.setOpacity(0.5)
       self.imageLabel.setGraphicsEffect(self.op)
       self.pictureWidget.pictureBoxLabel.setPixmap(QPixmap("sources/picture_boxes.png"))
       self.pictureWidget.pictureLabel.setPixmap(
           QPixmap.fromImage(images[0]).scaled(531, 454, Qt.IgnoreAspectRatio))
       self.afterWidget.detectFaceImageLabel.setPixmap(QPixmap.fromImage(images[1]).scaled(240, 240, Qt.IgnoreAspectRatio))
       self.afterWidget.detectFaceImageLabel.setHidden(True)
       self.initAnimation1()

   def initAnimation1(self):
       self.animation = QPropertyAnimation(self.pictureWidget,b"geometry")
       self.animation.setDuration(1000)
       self.animation.setStartValue(QRect(300,135,594,454))
       self.animation.setEndValue(QRect(1246,255,1,1))
       self.animation.start()

   def initAnimation2(self):
       self.afterWidget.startAnimation2()



class PictureWidget(QWidget):
    def __init__(self, parent=None):
        super(PictureWidget, self).__init__(parent)
        self.pictureBoxLabel = QLabel("", self)
        self.pictureBoxLabel.setGeometry(0, 0, 594, 454)
        self.pictureBoxLabel.setAlignment(Qt.AlignLeft)
        self.pictureLabel = QLabel("", self)
        self.pictureLabel.setGeometry(30, 29, 531, 379)
        self.pictureLabel.setAlignment(Qt.AlignLeft)



class AfterDetectWidget(QWidget):
    def __init__(self, parent=None):
        super(AfterDetectWidget,self).__init__(parent)
        self.backgroundLabel = QLabel("", self)
        self.backgroundLabel.setGeometry(0, 0, 400, 765)
        self.backgroundLabel.setPixmap(QPixmap("sources/bgbg.png"))



        self.detectFaceImageLabel = QLabel("", self)
        self.detectFaceImageLabel.setGeometry(76, 185, 240, 240)


        self.faceImageLabel = QLabel("", self)
        self.faceImageLabel.setGeometry(26, 137, 340, 340)
        facePixmap = QPixmap()
        facePixmap.load("sources/userBeforeDect.png")
        self.faceImageLabel.setPixmap(facePixmap)



        self.welcomeLabel = QLabel("", self)
        self.welcomeLabel.setGeometry(96, 529, 198, 90)
        welcomPixmap = QPixmap()
        welcomPixmap.load("sources/welcome.png")
        self.welcomeLabel.setPixmap(welcomPixmap)

    def startAnimation2(self):
        self.detectFaceImageLabel.setHidden(False)
        self.faceImageLabel.setPixmap(QPixmap("sources/after_detect.png"))
        self.animation2 = QPropertyAnimation(self.detectFaceImageLabel, b"geometry")
        self.animation2.setDuration(1000)
        self.animation2.setStartValue(QRect(196, 305, 0, 0))
        self.animation2.setEndValue(QRect(76, 185, 240, 240))
        self.animation2.start()













class ResultWidget(QWidget):
   def __init__(self, parent=None):
       super(ResultWidget, self).__init__(parent)

       self.backgroundLabel1 = QLabel(self)
       self.backgroundLabel1.setGeometry(0, 0, 540, 1080)
       self.backgroundLabel1.setPixmap(QPixmap("sources/history2.png"))

       self.ImageLabelArr = []
       self.TimeLabelArr = []
       textFont = QFont("Microsoft YaHei", 15, 75)
       for i in range(7):
           resultImageLabel = QLabel("",self)
           resultImageLabel.setGeometry(175,212+114*i,84,84)
           self.ImageLabelArr.append(resultImageLabel)

       self.backgroundLabel = QLabel(self)
       self.backgroundLabel.setGeometry(0, 0, 540, 1080)
       self.backgroundLabel.setPixmap(QPixmap("sources/history.png"))
       for i in range(7):
           savetimeLabel = QLabel("", self)
           savetimeLabel.setGeometry(280, 247+114*i, 180, 15)
           # savetimeLabel.setText("2019-06-14 10:00")
           savetimeLabel.setStyleSheet("color:#70644F;")
           savetimeLabel.setFont(textFont)
           self.TimeLabelArr.append(savetimeLabel)








