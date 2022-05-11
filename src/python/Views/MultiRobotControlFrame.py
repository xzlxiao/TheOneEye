from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QMessageBox, QInputDialog, QComboBox, QDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent, Qt
from Control import MainController, RobotController
from Common.DebugPrint import myDebug, get_current_function_name
from Views.ViewFrameBase import ViewFrameBase
from Views.XLabel import XLabel
from Entity.ImageHandle import ImageHandle
from Entity.RobotEpuck import RobotEpuck, RobotControlMode
from Algorithm.ImageProcRegister import getImageProcRegister
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from Algorithm.RobotPolicyRegister import getRobotPolicyRegister
from Algorithm.RobotPolicy.RobotPolicyBase import RobotPolicyBase
import PyQt5
from Entity.DataHandle import DataHandle
from functools import partial
import json
from Views import MessageShow

class MultiRobotControlFrame(ViewFrameBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(*arg)
        self.controller = MainController.getController()
        self.robot_controller = RobotController.RobotController()
        self.robot_controller.start()
        self.mDataHandle = DataHandle()
        self.controller.addDataHandle(self.mDataHandle)
        self.mLayout.addWidget(self.mDataHandle.image_label)
        self.mDataHandle.image_label.show()
        self.mRobotPolicy = None 

    def loadConfigFile(self, path):
        myDebug(self.__class__.__name__, get_current_function_name())
        print(path)
        with open(path, 'r') as f:
            data = json.load(f)
            self.setRobotPolicy(data["policy"])
            for robot_data in data["robots"]:
                self.addRobot(robot_data)

    def addRobot(self, robot_data: tuple):
        myDebug(self.__class__.__name__, get_current_function_name())
        if "type" not in robot_data.keys():
            MessageShow.warn("Warning", "The 'type' key is missing")
        else:
            robot_type = robot_data["type"]
            if robot_type == "RobotEpuck":
                print("add RobotEpuck")
                pass 
            elif robot_type == "RobotSimEpuck":
                print("add RobotSimEpuck")
                pass 
            else:
                print("robot type is wrong. ")

    def setRobotPolicy(self, policy: str):
        # if policy == "Robot"
        print("set policy ", policy)
        pass 

    def on_del_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().on_del_view()
        pass

    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(event.type(), ' ', QContextMenuEvent.MouseButtonRelease)
        # if event.type() == QContextMenuEvent.MouseButtonRelease:
        #     if event.button() == QtCore.Qt.RightButton:
        menu=self.mkQMenu()
        # set_robot_id_action = QAction('Set Robot ID', menu)
        # set_robot_id_action.triggered.connect(self.slot_set_robot_id)
        # menu.addAction(set_robot_id_action)
        menu.exec_(event.globalPos())

    def on_key_press(self, key_event):
        # if self.mRobot.mState == RobotControlMode.RemoteControl:
        #     if key_event.key() == Qt.Key_A:
        #         self.mRobot.setSpeed(-100, 100)
        #         print('Key_A')
        #     elif key_event.key() == Qt.Key_W:
        #         self.mRobot.setSpeed(500, 500)
        #         print('Key_W')
        #     elif key_event.key() == Qt.Key_D:
        #         self.mRobot.setSpeed(100, -100)
        #         print('Key_D') 
        #     elif key_event.key() == Qt.Key_S:
        #         self.mRobot.setSpeed(-500, -500)
        #         print('Key_S') 
        #     elif key_event.key() == Qt.Key_Space:
        #         self.mRobot.setSpeed(0, 0)
        #         print('Key_Space')
        pass