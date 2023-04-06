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
import os
from Common.DebugPrint import myDebug, get_current_function_name
import sys
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import platform
from datetime import datetime
import math
sys.path.append("../")

class Common:
    is_win = (platform.system() == "Windows")
    is_x86 = (platform.architecture()[0] == '32bit')
    is_darwin = (platform.architecture()[0] == 'Darwin')
    is_Linux = (platform.system() == "Linux")
    def __init__(self):
        pass
    
    @staticmethod
    def mkdir(dir):
        if os.path.exists(dir):
            return False
        else:
            os.makedirs(dir)
            return True

    @staticmethod
    def getTime(fmt=r"%Y-%m-%d, %H:%M:%S:%f") -> str:
        now = datetime.now()
        date_time = now.strftime(fmt)
        return date_time

    @staticmethod
    def getDirTime() -> str:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
        return date_time

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

    @staticmethod
    def setQLabelImage(img_dir, label):
        image = QPixmap()
        image.load(img_dir)
        width, height = label.width(), label.height()
        image = image.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # image_logo.scaled(self.labelLogo.width(), self.labelLogo.height(), Qt.KeepAspectRatio,Qt.SmoothTransformation)
        label.setPixmap(image)

    @staticmethod
    def angle_with_x_axis(v):
        """
        计算二维向量与 x 轴正向的夹角的函数
        
        参数：
        v -- 二维向量，以一个包含两个数字的列表或元组表示
        
        返回值：
        与 x 轴正向的夹角，以弧度表示
        """
        x, y = v
        return math.atan2(y, x)
    
    @staticmethod
    def distance(pt1, pt2):
        """
        计算两点间的距离
        :param pt1: list or np.array
        :param pt2: list or np.array
        :return:
        """
        if np.array(pt1, dtype=np.float32).ndim == 1:
            pt1 = np.array(pt1[0:3], dtype=np.float32)
            pt2 = np.array(pt2[0:3], dtype=np.float32)
            return np.linalg.norm(pt2 - pt1, ord=2)
        elif np.array(pt1, dtype=np.float32).ndim == 2 and np.array(pt2, dtype=np.float32).ndim == 1:
            pt1 = np.array(pt1, dtype=np.float32)
            pt2 = np.array(pt2, dtype=np.float32)
            return np.sqrt(np.power(pt2[0] - pt1[:, 0], 2) + np.power(pt2[1] - pt1[:, 1], 2))
        else:
            print("unsupported dim in  distance(pt1, pt2)")

class XRect:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y

