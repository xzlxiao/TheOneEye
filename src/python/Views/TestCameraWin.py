"""
       .==.        .==.
      //`^\\      //^`\\
     // ^ ^\(\__/)/^ ^^\\
    //^ ^^ ^/+  0\ ^^ ^ \\
   //^ ^^ ^/( >< )\^ ^ ^ \\
  // ^^ ^/\| v''v |/\^ ^ ^\\
 // ^^/\/ /  `~~`  \ \/\^ ^\\
 ----------------------------
BE CAREFULL! THERE IS A DRAGON.

Function：TestCameraWin

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：
pass

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.uic import loadUi
from Views import WinBase, XLabel
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")


class TestCameraWin(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(TestCameraWin, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/TestCameraWin2.ui', self)

        self.lbCameraShow: QLabel
        self.mCameraShow = XLabel.XLabel(self)

        self.mainlayout1.replaceWidget(self.lbCameraShow, self.mCameraShow)
        
        
        self.lbCameraShow.hide()
        self.mCameraShow.setStyleSheet("background-color: rgb(114, 159, 200);")
        self.mCameraShow.show()
        self.mReturnButton.setParent(self)

        self.id = 'TestCameraWin'
        self.name = 'TestCameraWin'
        self.mOpenCameraButton = QPushButton(self)
        self.mCloseCameraButton = QPushButton(self)
        self.mCamera = None

    def showEvent(self, event):
        self.setReturnButtonLoc()

    def hideEvent(self, event):
        pass

    def setCamera(self, camera):
        self.mCameraShow.hide()
        self.mainlayout1.replaceWidget(self.mCameraShow, camera.mViewCamera)
        self.mCameraShow = camera.mViewCamera
        self.mCamera = camera
        self.mCameraShow.show()
        self.mTestMovieShow = self.mCameraShow

    def setButton(self):
        style = """
            color: rgba(100, 178, 255, 230); 
            background-color: rgba(82, 84, 84, 50); 
            border:2px solid rgba(0, 178, 255, 230);
            """
        self.mOpenCameraButton.setStyleSheet(style)
        self.mCloseCameraButton.setStyleSheet(style)

        self.mOpenCameraButton.setFixedHeight(40)
        self.mOpenCameraButton.setMaximumWidth(200)
        self.mOpenCameraButton.setText(r"Open Camera")
        self.mOpenCameraButton.clicked.connect(self.on_OpenCameraButton)
        self.mOpenCameraButton.move(50, 50)
        self.mOpenCameraButton.show()

        self.mCloseCameraButton.setFixedHeight(40)
        self.mCloseCameraButton.setMaximumWidth(200)
        self.mCloseCameraButton.setText(r"Close Camera")
        self.mCloseCameraButton.clicked.connect(self.on_CloseCameraButton)
        self.mCloseCameraButton.move(50, 250)
        self.mCloseCameraButton.show()
        self.mReturnButton.show()

    def on_OpenCameraButton(self):
        if self.mCamera is not None:
            self.mCamera.openCamera()

    def on_CloseCameraButton(self):
        if self.mCamera is not None:
            self.mCamera.releaseCamera()