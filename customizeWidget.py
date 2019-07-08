from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QRect,QTimer,QPropertyAnimation


class ImageWidget(QWidget):
   def __init__(self, parent=None):
       super(ImageWidget, self).__init__(parent)
       self.detecFaceResult = False
       self.startAnnotation1 = False
       self.startAnnotation2 = False

       self.imageTemp = None
       self.imageLabel = QLabel("", self)
       self.imageLabel.setGeometry(0, 0, 1020, 765)  # 一定要有个东西把它撑起来！！不然看不到
       self.imageLabel.setPixmap(QPixmap("sources/picture_test.jpg"))

       self.op = QGraphicsOpacityEffect()
       self.op.setOpacity(0.5)



       self.pictureWidget = PictureWidget(self)
       self.pictureWidget.setGeometry(300,135,594,454)

       self.backgroundLabel = QLabel("", self)
       self.backgroundLabel.setGeometry(1020, 0, 1420 - 1020, 765)



       self.faceImageLabel = QLabel("", self)
       self.faceImageLabel.setGeometry(1046, 137, 340, 340)
       facePixmap = QPixmap()
       facePixmap.load("sources/userBeforeDect.png")
       self.faceImageLabel.setPixmap(facePixmap)

       self.detectFaceImageLabel = QLabel("", self)
       self.detectFaceImageLabel.setGeometry(1046, 137, 340, 340)


       self.welcomeLabel = QLabel("", self)
       self.welcomeLabel.setGeometry(1116, 529, 198, 80)
       welcomPixmap = QPixmap()
       welcomPixmap.load("sources/welcome.png")
       self.welcomeLabel.setPixmap(welcomPixmap)

   def setPictureHidden(self):
       self.op.setOpacity(1)
       self.imageLabel.setGraphicsEffect(self.op)
       self.pictureWidget.setHidden(True)
       self.pictureWidget.setHidden(True)


   def setPictireShow(self,image):
       self.pictureWidget.setHidden(False)
       self.op.setOpacity(0.5)
       self.imageLabel.setGraphicsEffect(self.op)
       self.pictureWidget.pictureBoxLabel.setPixmap(QPixmap("sources/picture_boxes.png"))
       self.pictureWidget.pictureLabel.setPixmap(
           QPixmap.fromImage(image).scaled(531, 379, Qt.KeepAspectRatioByExpanding))
       self.initAnimation1()

   def initAnimation1(self):
       self.animation = QPropertyAnimation(self.pictureWidget,b"geometry")
       self.animation.setDuration(1000)
       self.animation.setStartValue(QRect(300,135,594,454))
       self.animation.setEndValue(QRect(1246,255,1,1))
       self.animation.start()

   def initAnimation2(self,image):
       self.detectFaceImageLabel.setPixmap(QPixmap.fromImage(image).scaled(340, 340, Qt.KeepAspectRatioByExpanding))
       self.animation2 = QPropertyAnimation(self.detectFaceImageLabel,b"geometry")
       self.animation2.setDuration(1000)
       self.animation2.setStartValue(QRect(1220, 310, 1, 1))
       self.animation2.setEndValue(QRect(1130, 220, 180, 180))
       self.animation2.start()



class PictureWidget(QWidget):
    def __init__(self, parent=None):
        super(PictureWidget, self).__init__(parent)
        self.pictureBoxLabel = QLabel("", self)
        self.pictureBoxLabel.setGeometry(0, 0, 594, 454)
        self.pictureBoxLabel.setAlignment(Qt.AlignLeft)
        self.pictureLabel = QLabel("", self)
        self.pictureLabel.setGeometry(30, 29, 531, 379)
        self.pictureLabel.setAlignment(Qt.AlignLeft)

















class ResultWidget(QWidget):
   def __init__(self, parent=None):
       super(ResultWidget, self).__init__(parent)

       self.userfacePixmap = QPixmap("sources/picture_test.jpg")
       self.userfacePixmap = self.userfacePixmap.scaled(84,84,Qt.KeepAspectRatioByExpanding)



       textFont = QFont("Microsoft YaHei", 15, 75)
       self.savetimeLabel = QLabel("",self)
       self.savetimeLabel.setGeometry(102,35,161,15)
       self.savetimeLabel.setText("2019-06-14 10:00")
       self.savetimeLabel.setStyleSheet("color:#70644F;")
       self.savetimeLabel.setFont(textFont)

   def paintEvent(self, a0:QPaintEvent):
       painter = QPainter(self)
       path = QPainterPath()
       path.addEllipse(0, 0, 84,84)
       painter.setClipPath(path);
       painter.drawPixmap(0, 0, 84, 84, self.userfacePixmap)



