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

Function：NewControlWin

Modules：
pass

(c) 肖镇龙(xzl) 2023

"""
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QListView
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QStringListModel, Qt, QTimer
from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie

from PyQt5.uic import loadUi
from Views import WinBase, HomePageMainView
from Common.Common import Common
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
from Control import MainController
from Entity.RadioButtonGroup.RadioButtonGroup import RadioButtonGroup
from Entity.RadioButtonGroup.RadioButton import RadioButton
import sys
sys.path.append("../")

class HomePage(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(HomePage, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/HomePage.ui', self)

        self.id = 'HomePage'
        self.name = 'HomePage'

        self.mFrameViewArea = HomePageMainView.HomePageMainView(self)

        self.gridLayoutViews.replaceWidget(self.frameViewArea, self.mFrameViewArea)
        self.mFrameViewArea.show()
        # self.mFrameViewArea.setMinimumSize(500, 0)

        self.frameViewArea.hide()
        self.frameViewArea.destroy()

        self.mkConnect()

    def getViewNameList(self):
        return self.mFrameViewArea.getViewNameList()
    
    def mkConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())

    def showEvent(self, event):
        pass
        # view_size = self.width()/4
        # self.lbViewState.setMaximumSize(view_size, view_size)

    def hideEvent(self, event):
        pass


   
    # def setReturnButtonLoc(self):
    #     self.mReturnButton.move(self.width() / 10, self.height() * 8 / 10)

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)


