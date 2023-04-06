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

Function：ContentsNavWin

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
from PyQt5.QtGui import QPixmap, QResizeEvent

from PyQt5.uic import loadUi
from Views import WinBase, XLabel
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")


class ContentsNavWin(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(ContentsNavWin, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/ContentsNavWin.ui', self)

        self.id = 'ContentsNavWin'
        self.name = 'ContentsNavWin'

        self.mImage_T = QPixmap()
        self.mImage_T.load('resource/icons/T.png')
        self.mImage_O = QPixmap()
        self.mImage_O.load('resource/icons/O.png')
        self.mImage_E = QPixmap()
        self.mImage_E.load('resource/icons/E.png')
        
        self.lbT.setAlignment(QtCore.Qt.AlignCenter)
        self.lbT.setPixmap(self.mImage_T.scaled(self.lbT.width(), self.lbT.height()))
        self.lbO.setAlignment(QtCore.Qt.AlignCenter)
        self.lbO.setPixmap(self.mImage_O.scaled(self.lbO.width(), self.lbO.height()))
        self.lbE.setAlignment(QtCore.Qt.AlignCenter)
        self.lbE.setPixmap(self.mImage_E.scaled(self.lbE.width(), self.lbE.height()))

        self.mkConnect()

    def mkConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.btnToTestForm: QPushButton
        self.btnToTestForm.clicked.connect(self.on_btnToTestForm)
        self.btnToMVForm.clicked.connect(self.on_btnToMVForm)
        self.btnToNewControlForm.clicked.connect(self.on_btnToNewControlForm)

    def on_btnToTestForm(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.signalChangeWin.emit('TestCameraWin')

    def on_btnToMVForm(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.signalChangeWin.emit('MachineVisionWin')

    def on_btnToNewControlForm(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.signalChangeWin.emit('NewControlWin')

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)