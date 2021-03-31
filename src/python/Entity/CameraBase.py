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

Function：CameraBase

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
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from PyQt5.QtWidgets import QWidget


class CameraBase(QWidget):
    def __init__(self, *args):
        super(CameraBase, self).__init__(*args)
        self.mCameraId = -1

    def openCamera(self):
        pass

    def releaseCamera(self):
        pass

    def setCameraID(self, id):
        self.mCameraId = id

    def getImageFlow(self):
        pass
