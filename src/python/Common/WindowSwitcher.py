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

Function：窗口切换器

Modules：
pass

(c) 肖镇龙(xzl) 2023
"""
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLayout
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QResizeEvent

class WindowSwitcher:
    def __init__(self) -> None:
        self.mCurrentWindow:QWidget = None 
        self.mMainLayout:QLayout = None
    
    def setMainLayout(self, main_layout:QLayout):
        self.mMainLayout = main_layout

    def switchTo(self, win:QWidget):
        
        if self.mCurrentWindow is not None and self.mCurrentWindow is not win:
            self.mMainLayout.replaceWidget(self.mCurrentWindow, win)
            self.mCurrentWindow.hide()
        else:
            self.mMainLayout.addWidget(win)

        self.mCurrentWindow = win 
        self.mCurrentWindow.show()

    def getCurrentWin(self)->QWidget:
        return self.mCurrentWindow