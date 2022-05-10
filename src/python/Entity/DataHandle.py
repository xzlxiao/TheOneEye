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

Function：数据处理

Modules：
pass

(c) 肖镇龙(xzl) 2022

Dependencies：

Updating Records:

"""
import copy
import threading
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")
sys.path.append("./")
from functools import partial
from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer, QThread, QObject
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings
import numpy as np
from Common.Common import Common
from Views import XLabel
import copy
from Entity.HandleBase import HandleBase


class DataHandle(HandleBase):
    def __init__(self) -> None:
        super().__init__()
        self.image_label.mBackImage.load("resource/images/multi_robot.jpg")
        self.image_label.hide()

    def data_process(self):
        pass