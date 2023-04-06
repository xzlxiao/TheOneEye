from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox, QDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent, Qt
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Views.ImageProcViewBase import ImageProcViewBase
from Views.XLabel import XLabel
from Entity.ImageHandle import ImageHandle
from Entity.RobotEpuck import RobotEpuck, RobotControlMode
from Views.RobotFrame import RobotFrame
from Algorithm.ImageProcRegister import getImageProcRegister
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from Algorithm.RobotPolicyRegister import getRobotPolicyRegister
from Algorithm.RobotPolicy.RobotPolicyBase import RobotPolicyBase
import PyQt5

from functools import partial

class RobotFrameTest(RobotFrame):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(*arg)
        self.mViewType = 'RobotFrameTest'

    def setRobot(self, robot:RobotEpuck):
        super().setRobot(robot)
        robot.isTestRobot = True
        self.signalVisibleChanged.emit()

    def getDepict(self):
        '''
        获取当前视图的文字描述
        '''
        if self.mRobot is None:
            return '%s(ID:%d, isVisible:%d)'%(self.getViewType(), self.getId(), self.getVisibleState())
        else:
            return '%s(ID:%d, isVisible:%d, RobotID: %d)'%(self.getViewType(), self.getId(), self.getVisibleState(), self.mRobot.mId)


    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        menu=self.mkQMenu()
        set_robot_id_action = QAction('Set Robot ID', menu)
        set_robot_id_action.triggered.connect(self.slot_set_robot_id)
        menu.addAction(set_robot_id_action)
        control_list = QMenu(menu)
        control_list.setTitle('Control Mode')
        remote_control_action = QAction('Remote Control', control_list)
        remote_control_action.triggered.connect(partial(self.setRobotState, RobotControlMode.RemoteControl))
        control_list.addAction(remote_control_action)
        policy_control_action = QAction('Policy Control', control_list)
        policy_control_action.triggered.connect(partial(self.setRobotState, RobotControlMode.PolicyControl))
        control_list.addAction(policy_control_action)
        menu.addMenu(control_list)
        data_set_list = QMenu(menu)
        menu.exec_(event.globalPos())
