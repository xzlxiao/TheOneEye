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

Function：Read configure files

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QMainWindow, QFrame, QWidget, QGridLayout, QMenu, QAction
import numpy as np
import cv2
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QMovie, QResizeEvent, QMouseEvent, QContextMenuEvent
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from PyQt5.uic import loadUi
from Views import WinBase, XLabel
import math
from Common.DebugPrint import myDebug, get_current_function_name
from Common.XSetting import XSetting
from Common.Common import XRect
from Views.MainWindow import MainWindow
from Views.XLabel import XLabel
from Views import TestCameraWin, ContentsNavWin, MachineVisionWin
from Entity.CameraInterface import CameraInterface
from Control import MainController
import sys
sys.path.append("../")

class ViewController(QObject):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(ViewController, self).__init__(*args)
        self.mMainWin = MainWindow()
        self.mMainFrame = QFrame(self.mMainWin)
        self.mCurrentWin = None
        self.mMainLayout = QGridLayout(self.mMainFrame)
        self.mFrameList = []

        self.mTestCamera = CameraInterface()
        self.mTestMovieShow = None
        self.windowLoad()

        self.mCamregister = []
        self.mCamregister.append(self.on_add_camera0_view)
        self.mCamregister.append(self.on_add_camera1_view)
        self.mCamregister.append(self.on_add_camera2_view)
        self.mCamregister.append(self.on_add_camera3_view)
        self.mCamregister.append(self.on_add_camera4_view)

# 方法
    def windowLoad(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mMainFrame.setGeometry(0, 0, self.mMainWin.mCentralWidget.height(),
                                    self.mMainWin.mCentralWidget.width())
        if XSetting.isShowBorder:
            self.mMainFrame.setStyleSheet("border:2px solid rgba(255, 0, 0, 1);")
        self.mMainFrame.show()

        self.windowsInstall(ContentsNavWin.ContentsNavWin)
        self.windowsInstall(MachineVisionWin.MachineVisionWin)

        ### 摄像头测试 begin
        test_camera_win = self.windowsInstall(TestCameraWin.TestCameraWin)
        test_camera_win.setCamera(self.mTestCamera)
        test_camera_win.setButton()
        ### 摄像头测试 end

        self.eventFilterInstall()

    def windowsInstall(self, win_type):
        '''
        子窗口装载器
        :param win_type: 窗口类型
        :return:
        '''
        myDebug(self.__class__.__name__, get_current_function_name())
        win = win_type(self.mMainFrame)
        win.signalChangeWin.connect(self.slotChangeWin)
        win.signalReturn.connect(self.slotReturnWin)
        win.hide()
        self.mFrameList.append(win)
        return win

    def eventFilterInstall(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mMainWin.installEventFilter(self)
        self.mFrameList[1].frameViewArea.installEventFilter(self)

    def start(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mMainWin.show()
        movie = QMovie("resource/images/background001.gif")
        for label_i in self.mMainWin.mlbBackgroundList:
            label_i.setMovie(movie)
            label_i.setScaledContents(True)
        movie.start()

    def navigateTo(self, win_name: str):
        myDebug(self.__class__.__name__, get_current_function_name())
        isFind = False
        for iter in self.mFrameList:
            if win_name.strip() == iter.name:
                self.windowSwitch(iter)
                isFind = True

        if not isFind:
            raise Exception("Fail to switch window. The name of win isn't exited, please checking.")

    def windowSwitch(self, win: QWidget):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mCurrentWin: QFrame
        if self.mCurrentWin is not None:
            self.mMainLayout.replaceWidget(self.mCurrentWin, win)
            self.mCurrentWin.hide()
        else:
            self.mMainLayout.addWidget(win)
        self.mCurrentWin = win
        self.mCurrentWin.show()

    def getShowRect(self, src_image: np.ndarray, width_crop: int, height_crop: int) -> XRect:
        myDebug(self.__class__.__name__, get_current_function_name())
        ret = XRect()
        gui_wh_ratio = float(width_crop) / float(height_crop)
        img_wh_ratio = float(src_image.size().width) / float(src_image.size().height)
        if gui_wh_ratio > img_wh_ratio:
            ret.width = src_image.shape[1]
            ret.height = src_image.shape[0]
            ret.x = 0
            ret.y = int(math.floor(float(src_image.shape[0] - ret.height)/2.0))
        else:
            ret.height = src_image.shape[0]
            ret.width = int(float(ret.height) / float(height_crop) * float(width_crop))

            ret.x = int(math.floor((float(src_image.shape[1]) - float(ret.width))/2.0))
            ret.y = 0
        return ret

    def resizeImage(self, image_: np.ndarray, width_crop: int, height_crop: int) -> np.ndarray:
        myDebug(self.__class__.__name__, get_current_function_name())
        show_rect = self.getShowRect(image_, width_crop, height_crop)
        image_ = image_[show_rect.y:show_rect.height, show_rect.x:show_rect.width]
        return cv2.resize(image_, (width_crop, height_crop))

# 事件
    def eventFilter(self, watched: 'QObject', event: 'QEvent') -> bool:
        # myDebug(self.__class__.__name__, get_current_function_name())
        isEventGot = False
        if watched is self.mMainWin:
            if event.type() == QResizeEvent.Resize:
                self.mMainFrame.resize(self.mMainWin.mCentralWidget.width(), self.mMainWin.mCentralWidget.height())
                if self.mCurrentWin is not None:
                    self.mCurrentWin.setReturnButtonLoc()
                isEventGot = True
        elif watched is self.mFrameList[1].frameViewArea:
            if event.type() == QContextMenuEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.RightButton:
                    self.event_frameViewArea_menu(event)

        return isEventGot
    
    def event_frameViewArea_menu(self, event):
        menu=QMenu(self.mFrameList[1].frameViewArea)
        camera_list = QMenu(menu)
        camera_list.setTitle('新建相机视图')
        controller = MainController.getController()
        camera_names = controller.mCameraController.getAvailableCameraNames()
        for ind, name in enumerate(camera_names):
            cam_action = QAction(name, camera_list)
            cam_action.triggered.connect(self.mCamregister[ind])
            camera_list.addAction(cam_action)
        menu.addMenu(camera_list)
        menu.exec_(event.globalPos())

    def on_add_camera0_view(self):
        print('打开第0个相机')

    def on_add_camera1_view(self):
        print('打开第1个相机')

    def on_add_camera2_view(self):
        print('打开第2个相机')

    def on_add_camera3_view(self):
        print('打开第3个相机')

    def on_add_camera4_view(self):
        print('打开第4个相机')


    def slotChangeWin(self, win):
        myDebug(self.__class__.__name__, get_current_function_name())
        if isinstance(win, int):
            num = win
            if num < len(self.mFrameList):
                self.windowSwitch(self.mFrameList[num])
            else:
                raise Exception("Fail to switch window. The No. of win isn't exited, please checking.")
        elif isinstance(win, str):
            win_name = win
            isFind = False
            for iter in self.mFrameList:
                if win_name.strip() == iter.name:
                    self.windowSwitch(iter)
                    isFind = True
            if not isFind:
                raise Exception("Fail to switch window. The name of win isn't exited, please checking.")
        else:
            raise TypeError()

    def slotReturnWin(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.windowSwitch(self.mFrameList[0])