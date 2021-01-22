from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings
import numpy as np
from Common.Common import Common


class CameraInterface(CameraBase.CameraBase):
    def __init__(self, *args):
        super(CameraInterface, self).__init__(*args)
        # 定义相机实例对象并设置捕获模式
        self.mCamera = QCamera()
        self.mFrame = None
        self.mCamera.setCaptureMode(QCamera.CaptureViewfinder)
        self.mCameraOpened = False  # 设置相机打开状态为未打开
        self.mDisplayWidth = 450
        self.mDisplayHeight = 450
        self.mRate = 20

        # 设置取景器分辨率
        self.setDisplaySize(self.mDisplayWidth, self.mDisplayHeight)

        # 初始化取景器
        self.mViewCamera = QtMultimediaWidgets.QCameraViewfinder(self)
        self.mCamera.setViewfinder(self.mViewCamera)
        self.mCamera.setCaptureMode(QCamera.CaptureStillImage)

        # 设置图像捕获
        self.mCapture = QCameraImageCapture(self.mCamera)
        self.mCapture.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)  # CaptureToBuffer
        # self.mCapture.error.connect(lambda i, e, s: self.alert(s))
        self.mCapture.imageAvailable.connect(self.readFrame)

        self.mTimerImageGrab = QTimer(self)
        self.mTimerImageGrab.timeout.connect(self.timerImgGrab)

    def timerImgGrab(self):
        self.mCapture.capture('tmp.jpg')

    def readFrame(self, requestId, image):
        self.mFrame = Common.qImage2Numpy(image.image())

    def openCamera(self):
        if not self.mCameraOpened:
            self.mCamera.start()
            self.mTimerImageGrab.start(self.mRate)
            self.mCameraOpened = True

    def releaseCamera(self):
        if self.mCameraOpened:
            self.mCamera.stop()
            self.mCameraOpened = False

    def takePictures(self, path: str):
        self.mCapture.setCaptureDestination(QCameraImageCapture.CaptureToFile)
        self.mCapImg.capture(path)
        # print(r"save image to file: {}".format(path))
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