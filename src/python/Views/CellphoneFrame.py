from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox, QDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent, Qt
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Views.ImageProcViewBase import ImageProcViewBase
from Views.XLabel import XLabel
from Entity.ImageHandle import ImageHandle
from Entity.RobotCellphone import RobotCellphone
from Algorithm.ImageProcRegister import getImageProcRegister
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from Algorithm.RobotPolicyRegister import getRobotPolicyRegister
from Algorithm.RobotPolicy.RobotPolicyBase import RobotPolicyBase
import PyQt5

from functools import partial

class CellphoneFrame(ImageProcViewBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().__init__(*arg)
        self.mRobot: RobotCellphone = None 
        # self.insertOptionList('-----ImageProc-----', self.defaultFunc)
        # self.insertOptionList('添加图像处理模块', self.addImageProcFunc)
        # self.insertOptionList('------Policy------', self.defaultFunc)
        # self.insertOptionList('添加机器人Policy模块', self.addRobotPolicyFunc)

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
        self.insertOptionList('添加手机Policy模块', self.addRobotPolicyFunc)

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
        set_robot_id_action = QAction('Set Cellphone ID', menu)
        set_robot_id_action.triggered.connect(self.slot_set_robot_id)
        menu.addAction(set_robot_id_action)
        menu.exec_(event.globalPos())

    # def setRobotState(self, state: RobotControlMode):
    #     self.mRobot.mState = state
    
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

