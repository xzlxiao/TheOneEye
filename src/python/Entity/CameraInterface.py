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

Function：CameraInterface

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 09:38:15 xzl
"""
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings
import numpy as np
from Common.Common import Common
import time


class CameraInterface(CameraBase.CameraBase):
    def __init__(self, *args, camera_info=None):
        super(CameraInterface, self).__init__(*args)
        # 定义相机实例对象并设置捕获模式
        if camera_info:
            self.mCamera = QCamera(camera_info)
        else:
            self.mCamera = QCamera()
        self.mCamera.setCaptureMode(QCamera.CaptureViewfinder)
        self.mDisplayWidth = 800
        self.mDisplayHeight = 600
        self.mRate = 10

        # 设置取景器分辨率
        self.setDisplaySize(self.mDisplayWidth, self.mDisplayHeight)
        
        self.setRate(self.mRate)

        # 初始化取景器
        self.mViewCamera = QtMultimediaWidgets.QCameraViewfinder(self)
        self.mViewCamera.show()
        self.mCamera.setViewfinder(self.mViewCamera)
        self.mCamera.setCaptureMode(QCamera.CaptureStillImage)

        # 设置图像捕获
        self.mCapture = QCameraImageCapture(self.mCamera)
        if self.mCapture.isCaptureDestinationSupported(QCameraImageCapture.CaptureToBuffer):
            self.mCapture.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)  # CaptureToBuffer

        # self.mCapture.error.connect(lambda i, e, s: self.alert(s))
        self.mCapture.imageAvailable.connect(self.readFrame)

        self.mTimerImageGrab = QTimer(self)
        self.mTimerImageGrab.timeout.connect(self.timerImgGrab)
        # self.t1 = 0.0

    def timerImgGrab(self):
        self.mCapture.capture('tmp.jpg')

    def readFrame(self, requestId, image):
        self.mFrame = image.image().copy()

    def openCamera(self):
        if not self.mCameraOpened:
            self.mCamera.start()
            
            viewFinderSettings = QCameraViewfinderSettings()
            rate_range = self.mCamera.supportedViewfinderFrameRateRanges()
            if rate_range:
                viewFinderSettings.setMinimumFrameRate(rate_range[0].minimumFrameRate)
                viewFinderSettings.setMaximumFrameRate(rate_range[0].maximumFrameRate)
            else:
                viewFinderSettings.setMinimumFrameRate(1)
                viewFinderSettings.setMaximumFrameRate(self.mRate)
            self.mTimerImageGrab.start(1000/self.mRate)
            self.mCameraOpened = True
            

    def releaseCamera(self):
        if self.mCameraOpened:
            self.mCamera.stop()
            self.mCameraOpened = False
            self.signalReleased.emit()

    def takePictures(self, path: str):
        self.mCapture.setCaptureDestination(QCameraImageCapture.CaptureToFile)
        self.mCapImg.capture(path)
        self.mCapture.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)

    def takeVideo(self, path:str):
        pass

    def endTakeVideo(self):
        pass

    def setDisplaySize(self, display_width_:int, display_height_:int):
        self.mDisplayWidth = display_width_
        self.mDisplayHeight = display_height_
        viewFinderSettings = QCameraViewfinderSettings()
        viewFinderSettings.setResolution(self.mDisplayWidth, self.mDisplayHeight)
        self.mCamera.setViewfinderSettings(viewFinderSettings)

    def setRate(self, rate):
        self.mRate = rate 
        

    