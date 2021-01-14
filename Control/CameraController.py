from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")
import numpy as np
from enum import Enum
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QMovie, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QEvent


class XCameraType:
    X_USB_CAM = 0
    X_RealsenseD_CAM = 1
    X_RealsenseT_CAM = 2


class CameraController(QObject):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(CameraController, self).__init__(*args)
        self.mCameraList = []
        self.mCameraNum = 0

    def run(self):
        pass

    def CamerasDetect(self):
        pass

    def StartCamera(self, cam_id: int, camera_type: XCameraType):
        pass

    def releaseCamera(self, cam_id: int):
        pass

    def gotFrame(self, cam_id: int):
        pass