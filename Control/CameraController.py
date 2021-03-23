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

Function：The controller of cameras

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
import numpy as np
from enum import Enum
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QMovie, QResizeEvent
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from Entity.CameraInterface import CameraInterface
import copy
from Entity.CameraHandle import CameraHandle


class XCameraType:
    X_USB_CAM = 0
    X_RealsenseD_CAM = 1
    X_RealsenseT_CAM = 2



class CameraController(QObject):
    signalCamerasChanged = pyqtSignal()
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(CameraController, self).__init__(*args)
        self.mCameraList = []
        self.mCameraHandledImage = []
        self.mCameraAvailable = []
        self.mCameraNum = 0

    def run(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        self.CamerasDetect()
        for handle in self.mCameraHandledImage:
            handle.image_process()

    def CamerasDetect(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        detects = QCameraInfo.availableCameras()
        isChanged = False
        if len(self.mCameraAvailable) == len(detects):
            for i, data in enumerate(detects):
                if self.mCameraAvailable[i] != data:
                    isChanged = True
                    self.mCameraAvailable[i] = data
        else:
            isChanged = True
            self.mCameraAvailable = []
            for data in detects:
                self.mCameraAvailable.append(data)

        if isChanged:
            self.signalCamerasChanged.emit()

    def StartCamera(self, cam_id: int, camera_type: XCameraType):
        myDebug(self.__class__.__name__, get_current_function_name())
        if cam_id > len(self.mCameraAvailable):
            raise Exception('不存在第%d号摄像头' % cam_id)
        if camera_type == XCameraType.X_USB_CAM:
            self.mCameraList.append(CameraInterface(camera_info=self.mCameraAvailable[cam_id]))
            self.mCameraList[-1].openCamera()
            self.mCameraHandledImage.append(CameraHandle(self.mCameraList[-1]))
        else:
            raise Exception("暂不支持该型号摄像头")

    def releaseCamera(self, cam_id: int):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mCameraHandledImage.remove(cam_id)
        self.mCameraList[cam_id].releaseCamera()
        self.mCameraList.remove(cam_id)

    def getAvailableCameraNames(self):
        ret = []
        for i in self.mCameraAvailable:
            ret.append(i.description())

        return ret 
