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

Function：Common utils

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 09:38:15 xzl
"""
from Common.DebugPrint import myDebug, get_current_function_name
import sys
import numpy as np
from PyQt5.QtGui import QImage
import platform
sys.path.append("../")

class Common:
    is_win = (platform.system() == "Windows")
    is_x86 = (platform.architecture()[0] == '32bit')
    is_darwin = (platform.architecture()[0] == 'Darwin')
    is_Linux = (platform.system() == "Linux")
    def __init__(self):
        pass

    @staticmethod
    def getTime() -> str:
        pass

    @staticmethod
    def getSimilarity(A: np.ndarray, B: np.ndarray) -> bool:
        pass

    @staticmethod
    def qImage2Numpy(qimg: QImage, channels=3) -> np.ndarray:
        ptr = qimg.constBits()
        ptr.setsize(qimg.byteCount())
        mat = np.array(ptr).reshape(qimg.height(), qimg.width(), channels)
        return mat
    
    @staticmethod
    def numpy2QImage(img: np.ndarray) -> QImage:
        qimg = QImage(img.data.tobytes(), img.shape[1], img.shape[0], QImage.Format_ARGB32)
        return qimg

    @staticmethod
    def rgb565ToRgb888(img_src, rows, cols):
        img_src = np.reshape(img_src, (rows, cols, 2))
        img_dst = np.zeros((rows, cols, 3), dtype=np.uint8)
        img_dst[:, :, 0] = img_src[:, :, 0]&0xF8
        img_dst[:, :, 1] = (img_src[:, :, 0]&0x07)<<5 | (img_src[:, :, 1]&0xE0)>>3
        img_dst[:, :, 1] = (img_src[:, :, 1]&0x1F)<<3
        return img_dst

class XRect:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y

