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

Function：MainWindow

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：
pass

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.uic import loadUi
from Views import WinBase, XLabel
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name


class MainWindow(QMainWindow):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(MainWindow, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/MainWindow.ui', self)
        self.mlbBackgroundList = []
        self.mCentralWidget = self.centralwidget
        self.mlbBackgroundList.append(self.lbBackground1)
        self.mlbBackgroundList.append(self.lbBackground2)
        self.mlbBackgroundList.append(self.lbBackground3)
        self.mlbBackgroundList.append(self.lbBackground4)
        self.mlbBackgroundList.append(self.lbBackground5)
        self.mlbBackgroundList.append(self.lbBackground6)