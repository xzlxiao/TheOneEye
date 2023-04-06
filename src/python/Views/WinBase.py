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

Function：WinBase

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：
pass

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

class WinBase(QtWidgets.QWidget):
    signalReturn = pyqtSignal()
    signalChangeWin = pyqtSignal(str)
    def __init__(self, *args):
        super(WinBase, self).__init__(*args)
        self.id: str
        self.name: str
        self.mReturnButton = QPushButton()
        self.mReturnButton.setStyleSheet(
            """
            color: rgba(100, 178, 255, 230); 
            background-color: rgba(82, 84, 84, 50); 
            border:2px solid rgba(0, 178, 255, 230);
            """
        )
        self.mReturnButton.setFixedHeight(30)
        self.mReturnButton.setMaximumWidth(100)
        self.mReturnButton.setText(r"Return")
        self.mReturnButton.clicked.connect(self.on_ReturnButton)
        self.isStartBackMovie = True

    def windowLoad(self):
        pass

    def on_ReturnButton(self):
        self.signalReturn.emit()

    def setReturnButtonLoc(self):
        self.mReturnButton.move(self.width() * 0.5 / 10, self.height() * 9 / 10)