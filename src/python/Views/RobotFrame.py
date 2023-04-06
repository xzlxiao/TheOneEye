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
from Algorithm.ImageProcRegister import getImageProcRegister
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from Algorithm.RobotPolicyRegister import getRobotPolicyRegister
from Algorithm.RobotPolicy.RobotPolicyBase import RobotPolicyBase
import PyQt5

from functools import partial

class RobotFrame(ImageProcViewBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(*arg)
        self.mRobot: RobotEpuck = None 
        # self.insertOptionList('-----ImageProc-----', self.defaultFunc)
        # self.insertOptionList('添加图像处理模块', self.addImageProcFunc)
        # self.insertOptionList('------Policy------', self.defaultFunc)
        # self.insertOptionList('添加机器人Policy模块', self.addRobotPolicyFunc)

    def getDepict(self):
        '''
        获取当前视图的文字描述
        '''
        if self.mRobot is None:
            return '%s(ID:%d, isVisible:%d)'%(self.getViewType(), self.getId(), self.getVisibleState())
        else:
            return '%s(ID:%d, isVisible:%d, RobotID: %d, IP: %s)'%(self.getViewType(), self.getId(), self.getVisibleState(), self.mRobot.mId, self.mRobot.client_addr)

    def setRobot(self, robot):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mRobot = robot
        self.mImageHandle.setImageFlow(robot.mCamera)
        self.clearOptionList()
        if self.mRobot is not None:
            self.insertOptionList('%s [ID: %d]'% (robot.client_addr, robot.mId), self.defaultFunc, 0)
        else: 
            self.insertOptionList(robot.client_addr, self.defaultFunc, 0)
        self.insertOptionList('-----ImageProc-----', self.defaultFunc)
        self.insertOptionList('添加图像处理模块', self.addImageProcFunc)
        self.insertOptionList('------Policy------', self.defaultFunc)
        self.insertOptionList('添加机器人Policy模块', self.addRobotPolicyFunc)
        self.signalVisibleChanged.emit()

    def addRobotPolicyFunc(self, ind: int):
        myDebug(self.__class__.__name__, get_current_function_name())
        register = getRobotPolicyRegister()
        items = register.getNames()
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250)
        dialog.setWindowTitle('Set Input Flow for Improcessor')
        dialog.setComboBoxItems(items)
        dialog.textValueSelected.connect(lambda: self._addRobotPolicy(ind, register[dialog.findChild(QComboBox).currentIndex()]) if dialog.findChild(QComboBox).currentIndex() >= 0 else None)
        dialog.show()

    def _addRobotPolicy(self, ind:int, policy: RobotPolicyBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        policy.setRobot(self.mRobot)
        self.insertOptionList(policy.Name, self.addRobotPolicyFunc, ind)
        self.deleteOptionList(ind+1)
        self.signalFocusedChanged.emit(self, True)

    def on_del_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().on_del_view()
        self.mRobot.disconnect()
    
    def getInputFlow(self):
        return self.mRobot

    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(event.type(), ' ', QContextMenuEvent.MouseButtonRelease)
        # if event.type() == QContextMenuEvent.MouseButtonRelease:
        #     if event.button() == QtCore.Qt.RightButton:
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
        data_set_list.setTitle('数据流开关')
        data_stream_start = QAction('开启机器人返回的数据流', data_set_list)
        data_stream_start.triggered.connect(self.slot_robot_data_stream_start)
        data_set_list.addAction(data_stream_start)
        data_stream_stop = QAction('关闭机器人返回的数据流', data_set_list)
        data_stream_stop.triggered.connect(self.slot_robot_data_stream_stop)
        data_set_list.addAction(data_stream_stop)
        menu.addMenu(data_set_list)
        menu.exec_(event.globalPos())

    def setRobotState(self, state: RobotControlMode):
        self.mRobot.mState = state
    
    def slot_robot_data_stream_start(self):
        self.mRobot.isDataStreamOn = True 

    def slot_robot_data_stream_stop(self):
        self.mRobot.isDataStreamOn = False

    def slot_set_robot_id(self):
        self.parent().releaseKeyboard()
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250) 
        dialog.setWindowTitle('Set Input Flow for Improcessor')
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText('请输入……（机器人的ID）')
        dialog.setTextValue('7')
        dialog.setOkButtonText('Ok')
        dialog.setCancelButtonText('Cancel')
        if dialog.exec_() == QDialog.Accepted:
            id = dialog.textValue()
            if self.mRobot:
                self.mRobot.mId = int(id)
                self.deleteOptionList(0)
                self.insertOptionList('%s [ID: %d]'% (self.mRobot.client_addr, self.mRobot.mId), self.defaultFunc, 0)
                self.parent().grabKeyboard()
                self.signalFocusedChanged.emit(self, True)
        else:
            print("dialog canceled")
        dialog.show()

    def on_key_press(self, key_event):
        if self.mRobot.mState == RobotControlMode.RemoteControl:
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
            elif key_event.key() == Qt.Key_P:
                pass 
            elif key_event.key() == Qt.Key_Escape:
                self.parent().releaseKeyboard()
                print('Key_Escape')