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
sys.path.append("../")

class Common:
    def __init__(self):
        pass

    @staticmethod
    def getTime() -> str:
        pass

    @staticmethod
    def getSimilarity(A: np.ndarray, B: np.ndarray) -> bool:
        pass

    @staticmethod
    def qImage2Numpy(qimg: QImage) -> np.ndarray:
        ptr = qimg.constBits()
        ptr.setsize(qimg.byteCount())
        mat = np.array(ptr).reshape(qimg.height(), qimg.width(), 4)  # 注意这地方通道数一定要填4，否则出错
        return mat

class XRect:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y

