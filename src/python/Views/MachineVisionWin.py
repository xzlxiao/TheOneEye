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

Function：MachineVisionWin

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.uic import loadUi
from Views import WinBase, XLabel
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

class MachineVisionWin(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(MachineVisionWin, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/MachineVisionWin.ui', self)

        self.id = 'MachineVisionWin'
        self.name = 'MachineVisionWin'

        self.mReturnButton.setParent(self)
        self.mReturnButton.show()
        self.mkConnect()

    def mkConnect(self):
        pass

    def showEvent(self, event):
        self.setReturnButtonLoc()

    def hideEvet(self, event):
        pass

    # def setReturnButtonLoc(self):
    #     self.mReturnButton.move(self.width() / 10, self.height() * 8 / 10)