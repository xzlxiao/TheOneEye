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

Function：XLabel

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：
pass

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
import numpy as np
from Common.Common import get_current_function_name, Common
from Common.DebugPrint import myDebug
import platform
import sys
sys.path.append("../")


class XLabel(QLabel):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(XLabel, self).__init__(*args)
        self.mImage = None
        self.mBackImage = QPixmap()
        # self.mBackImage.load("resource/images/EyeOfSauron.jpeg")
        if platform.system() == 'Darwin':
            self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        else:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, e):
        # myDebug(self.__class__.__name__, get_current_function_name())
        if self.mImage is not None:
            painter = QPainter(self)
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            image_height = (self.width()-4)*self.mImage.height()/self.mImage.width()
            painter.drawPixmap(2, self.height()/2-image_height/2, self.width()-4, image_height, QtGui.QPixmap.fromImage(self.mImage))
            painter.restore()
        else:
            painter = QPainter(self)
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            image_height = (self.width()-4)*self.mBackImage.height()/self.mBackImage.width()
            painter.drawPixmap(2, self.height()/2-image_height/2, self.width()-4, image_height, self.mBackImage)
            painter.restore()