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
from PyQt5.QtWidgets import QSizePolicy, QLabel
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QMovie, QResizeEvent
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from Entity.CameraInterface import CameraInterface
import copy
# from Entity.CameraHandle import CameraHandle


class XCameraType:
    X_USB_CAM = 0
    X_RealsenseD_CAM = 1
    X_RealsenseT_CAM = 2


class CameraController(QObject):
    signalCamerasChanged = pyqtSignal()
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(CameraController, self).__init__(*args)
        self.mCameraList = {}
        # self.mCameraHandledImage = {}
        self.mCameraAvailable = []
        self.mCameraNum = 0

    def run(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        self.CamerasDetect()
        # for handle in self.mCameraHandledImage.values():
        #     handle.image_process()

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

    def startCamera(self, cam_id: int, camera_type:XCameraType=XCameraType.X_USB_CAM):
        myDebug(self.__class__.__name__, get_current_function_name())
        # if cam_id > len(self.mCameraAvailable):
        #     raise Exception('不存在第%d号摄像头' % cam_id)
        # if camera_type == XCameraType.X_USB_CAM:
        #     if cam_id in self.mCameraList.keys():
        #         pass
        #     else:
        #         self.mCameraList[cam_id] = CameraInterface(camera_info=self.mCameraAvailable[cam_id])
        #         self.mCameraList[cam_id].openCamera()
        #         self.mCameraHandledImage[cam_id] = CameraHandle(self.mCameraList[cam_id])
        # else:
        #     raise Exception("暂不支持该型号摄像头")
        
        if cam_id > len(self.mCameraAvailable):
            raise Exception('不存在第%d号摄像头' % cam_id)
        if camera_type == XCameraType.X_USB_CAM:
            cam_index = len(self.mCameraList)
            self.mCameraList[cam_index] = CameraInterface(camera_info=self.mCameraAvailable[cam_id])
            self.mCameraList[cam_index].setID(cam_index)
            self.mCameraList[cam_index].openCamera()
            self.mCameraList[cam_index].mViewCamera.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            self.mCameraList[cam_index].setCameraName(self.mCameraAvailable[cam_id].description())
            # self.mCameraList[cam_index].mViewCamera.setStyleSheet("border:2px solid rgb(100, 100, 100);")
            # cam_name = self.mCameraAvailable[cam_id].description()
            # cam_name_label = QLabel(self.mCameraList[cam_index].mViewCamera)
            # cam_name_label.setText(cam_name)
            # cam_name_label.x = 0
            # cam_name_label.y = 0
            # cam_name_label.setStyleSheet("color: rgb(255, 0, 0);border:0px solid rgba(100, 100, 100, 0);")
            # cam_name_label.show()
            
            # self.mCameraHandledImage[cam_index] = CameraHandle(self.mCameraList[cam_index])
        else:
            raise Exception("暂不支持该型号摄像头")

    def releaseCamera(self, cam_index: int):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(cam_index)
        # self.mCameraHandledImage.pop(cam_index)
        self.mCameraList[cam_index].releaseCamera()
        self.mCameraList.pop(cam_index)

    def releaseAllCamera(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        for i in range(len(self.mCameraList)):
            self.releaseCamera(i)

    def getAvailableCameraNames(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        ret = []
        for i in self.mCameraAvailable:
            ret.append(i.description())

        return ret 

    def getCameraList(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        return self.mCameraList.values()

    def getCamera(self, id):
        myDebug(self.__class__.__name__, get_current_function_name())
        if id >= len(self.mCameraList) or id < 0:
            return None 
        else:
            return self.mCameraList[id]