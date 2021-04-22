from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent, Qt
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Views.ImageProcViewBase import ImageProcViewBase
from Views.XLabel import XLabel
from Entity.ImageHandle import ImageHandle
from Entity.RobotEpuck import RobotEpuck
from Algorithm.ImageProcRegister import getImageProcRegister
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import PyQt5

class RobotFrame(ImageProcViewBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(*arg)
        self.mRobot: RobotEpuck = None 
        self.insertOptionList('添加图像处理模块', self.addImageProcFunc)

    def setRobot(self, robot):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mRobot = robot
        self.mImageHandle.setImageFlow(robot.mCamera)
        self.deleteOptionList(0)
        self.insertOptionList(robot.client_addr, self.defaultFunc, 0)
        self.insertOptionList('添加图像处理模块', self.addImageProcFunc)

    def on_del_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().on_del_view()
        self.mRobot.disconnect()
    
    def getInputFlow(self):
        return self.mRobot

    def on_key_press(self, key_event):
        if self.mRobot.mState == 0:
            if key_event.key() == Qt.Key_A:
                self.mRobot.setSpeed(-100, 100)
                print('Key_A')
            elif key_event.key() == Qt.Key_W:
                self.mRobot.setSpeed(500, 500)
                print('Key_W')
            elif key_event.key() == Qt.Key_D:
                self.mRobot.setSpeed(100, -100)
                print('Key_D') 
            elif key_event.key() == Qt.Key_S:
                self.mRobot.setSpeed(-500, -500)
                print('Key_S') 
            elif key_event.key() == Qt.Key_Space:
                self.mRobot.setSpeed(0, 0)
                print('Key_Space')