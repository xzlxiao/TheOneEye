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

Function：CameraHandle 摄像头图像处理

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-03-23 10:43:40 xzl
"""

from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")
sys.path.append("./")

from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings
import numpy as np
from Common.Common import Common
from Views import XLabel
from Entity.CameraInterface import CameraInterface
import copy

class CameraHandle:
    def __init__(self, camera: CameraInterface):
        self.image_label = XLabel.XLabel()
        self.image_label.hide()
        self.image_process = []     # 函数指针列表 func(image_src)->image_dst
        self.mCamera = camera

    def image_process(self):
        if self.mCamera.mFrame is not None:
            if len(self.image_process):
                image = copy.deepcopy(self.mCamera.mFrame)
                for func in self.image_process:
                    image = func(image)
                self.image_label.mImage = image
            else:
                self.image_label.mImage = copy.deepcopy(self.mCamera.mFrame)