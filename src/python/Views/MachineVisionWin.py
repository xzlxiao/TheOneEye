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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QListView
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QStringListModel
from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie

from PyQt5.uic import loadUi
from Views import WinBase, MultiViewFrame
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
from Control import MainController
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

        self.mFrameViewArea = MultiViewFrame.MultiViewFrame(self)

        self.gridLayoutViews.replaceWidget(self.frameViewArea, self.mFrameViewArea)
        self.mFrameViewArea.show()
        self.mFrameViewArea.setMinimumSize(500, 0)
        
        
        self.frameViewArea.hide()
        self.frameViewArea.destroy()

        self.mSlm = QStringListModel()
        self.listViewOption.setModel(self.mSlm)

        movie = QMovie("resource/images/SE3.gif")
        # self.mImage_viewState = QPixmap()
        # self.mImage_viewState.load('resource/images/Grid4.png')
        
        # self.lbViewState.setAlignment(QtCore.Qt.AlignCenter)
        self.lbViewState.setMovie(movie)
        self.lbViewState.setScaledContents(True)
        view_size = self.width()/4
        self.lbViewState.setMaximumSize(view_size, view_size)
        self.lbViewState.setMaximumWidth(view_size)
        movie.start()
        
        self.mkConnect()

    def mkConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mReturnButton.clicked.connect(self.slot_return)
        self.mFrameViewArea.signalViewFocusChanged.connect(self.slot_view_focaus_changed)
        self.listViewOption.clicked.connect(self.on_clicked_list)

    def showEvent(self, event):
        self.setReturnButtonLoc()
        view_size = self.width()/4
        self.lbViewState.setMaximumSize(view_size, view_size)

    def hideEvet(self, event):
        pass

    def slot_view_focaus_changed(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFrameViewArea.mFocusedView:
            self.mSlm.setStringList(self.mFrameViewArea.mFocusedView.mOptionList)
        else:
            self.mSlm.setStringList([])

    def slot_return(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        controller = MainController.getController()
        camera_controller = controller.mCameraController 
        camera_controller.releaseAllCamera()
        self.mFrameViewArea.slot_clearSubview()
    # def setReturnButtonLoc(self):
    #     self.mReturnButton.move(self.width() / 10, self.height() * 8 / 10)

    def on_clicked_list(self, qModelIndex):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFrameViewArea.mFocusedView:
            self.mFrameViewArea.mFocusedView.mOptionFuncList[qModelIndex.row()]()

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        view_size = self.width()/4
        self.lbViewState.setMaximumSize(view_size, view_size)
