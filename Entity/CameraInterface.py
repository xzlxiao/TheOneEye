from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings


class CameraInterface(CameraBase):
    def __init__(self, *args):
        super(CameraInterface, self).__init__(*args)
        # 定义相机实例对象并设置捕获模式
        self.camera = QCamera()
        self.camera.setCaptureMode(QCamera.CaptureViewfinder)
        self.cameraOpened = False  # 设置相机打开状态为未打开
        self.display_width = 450
        self.display_height = 450

        # 设置取景器分辨率
        viewFinderSettings = QCameraViewfinderSettings()
        viewFinderSettings.setResolution(self.display_width, self.display_height)
        self.camera.setViewfinderSettings(viewFinderSettings)

        # 初始化取景器
        self.viewCamera = QtMultimediaWidgets.QCameraViewfinder(self)
        self.camera.setViewfinder(self.viewCamera)

    def readFrame(self):
        pass

    def openCamera(self):
        pass

    def releaseCamera(self):
        pass

    def takePictures(self, path:str):
        pass

    def takeVideo(self, path:str):
        pass

    def endTakeVideo(self):
        pass

    def setDisplaySize(self, display_width_:int, display_height_:int):
        self.display_width = display_width_
        self.display_height = display_height_