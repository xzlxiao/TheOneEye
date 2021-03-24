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
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
import numpy as np
from Common.Common import get_current_function_name
from Common.DebugPrint import myDebug
import sys
sys.path.append("../")


class XLabel(QLabel):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(XLabel, self).__init__(*args)
        self.mImage = None

    def paintEvent(self, e):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mImage is not None:
            painter = QPainter()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.drawPixmap(self.rect(), QtGui.QPixmap.fromImage(self.mImage))