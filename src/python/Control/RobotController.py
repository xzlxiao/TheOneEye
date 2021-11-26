from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")
import numpy as np
from enum import Enum
from PyQt5.QtWidgets import QSizePolicy, QLabel
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtGui import QMovie, QResizeEvent
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from Entity.CameraInterface import CameraInterface
from Entity.RobotEpuck import RobotEpuck
from PyQt5.QtWidgets import QWidget
import copy
# from Entity.CameraHandle import CameraHandle
import time
import threading
from Control import MainController

class RobotController(QWidget):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(*args)
        self.mRobotList = []
        self.mRobotRunTimer = QtCore.QTimer(self)
        self.mRobotRunTimer.timeout.connect(self.run)

    def start(self):
        self.mRobotRunTimer.start(30)

    def addRobot(self, robot_type=RobotEpuck):
        myDebug(self.__class__.__name__, get_current_function_name())
        robot = robot_type(self, self.mRobotList)
        self.mRobotList.append(robot)
        # controller = MainController.getController()
        # controller.mCameraController
    
    def releaseRobot(self, robot: int):
        robot_index = self.mRobotList.index(robot)
        self.mRobotList[robot_index].disconnect()
        self.mRobotList.pop(robot_index)

    def getRobot(self, num):
        myDebug(self.__class__.__name__, get_current_function_name())
        assert num < len(self.mRobotList)
        return self.mRobotList[num]

    def update(self):
        pass

    def run(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        self.update()
        for robot in self.mRobotList:
            robot.update()
            print(robot.mPos)
            print(robot.mRobotEulerAngle)