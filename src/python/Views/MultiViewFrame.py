from functools import partial

import PyQt5
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QDialog, QGridLayout, QSizePolicy, QVBoxLayout, QListView, QInputDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent, Qt
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Entity.CameraInterface import CameraInterface
from Entity.RobotEpuck import RobotEpuck
from Entity.RobotVEpuck import RobotVEpuck
from Entity.RobotTwinsEpuck import RobotTwinsEpuck
from Views.CameraViewFrame import CameraViewFrame
from Views.CellphoneFrame import CellphoneFrame
from Views.ImageProcViewFrame import ImageProcViewFrame
from Views.ViewFrameBase import ViewFrameBase
from Views.RobotFrame import RobotFrame
from Views.RobotFrameTest import RobotFrameTest
from Views.MultiRobotControlFrame import MultiRobotControlFrame
from Control.CameraController import XCameraType
import copy

from enum import Enum

from Entity.RobotCellphone import RobotCellphone

class ViewShowState(Enum):
    viewMaximized = 0
    viewMinimized = 1
    viewEncircled = 2

class MultiViewFrame(QFrame):
    signalViewFocusChanged = pyqtSignal()
    signalViewShowStateChanged = pyqtSignal(ViewShowState)
    signalViewListChanged = pyqtSignal()
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(MultiViewFrame, self).__init__(*args)
        self.setStyleSheet("color: rgb(0, 243, 255);background-color: rgba(255, 255, 255, 0); border:2px solid rgb(0, 178, 255);")
        self.mMainLayout = QGridLayout(self)
        self.mMainLayout.setContentsMargins(1, 1, 1, 1)
        self.mMainLayout.setSpacing(1)

        self.mBackgound = QLabel(self)
        self.mBackgound.setGeometry(self.width()*0.5/3, self.height()*0.5/3, self.width()*2/3, self.height()*2/3)
        self.mBackgound.setStyleSheet("background-color: rgba(255, 255, 255, 0); border:0px solid rgb(0, 0, 0)")
        self.mBackgound.setAlignment(QtCore.Qt.AlignCenter)
        image = QPixmap("resource/images/earth.png")
        self.mBackgound.setPixmap(image.scaled(self.mBackgound.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.mBackgound.show()

        self.mFocusedView = None
        # self.mLastVisibleViewList = []
        self.mViewList = []
        self.isViewMaximizedStateChanged = False
        self.mMaximizedView = None

    def getVisibleViewList(self):
        return [view for ind, view in enumerate(self.mViewList) if view.getVisibleState() if ind < 36]

    def mkQMenu(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        menu = QMenu(self)
        menu.setStyleSheet("""
        color: rgb(0, 243, 255);
        background-color: rgba(255, 255, 255, 0); 
        border:2px solid rgb(0, 108, 255);
        selection-background-color: rgba(183, 212, 255, 150);
        """
        )
        camera_list = QMenu(menu)
        camera_list.setTitle('新建相机视图')
        controller = MainController.getController()
        camera_names, camera_types = controller.mCameraController.getAvailableCameraNames()
        for ind, name in enumerate(camera_names):
            cam_action = QAction(name, camera_list)
            # cam_action.triggered.connect(self.mCameregister[ind])
            cam_action.triggered.connect(partial(self.on_add_camera_view, ind, camera_types[ind]))
            camera_list.addAction(cam_action)
        menu.addMenu(camera_list)

        add_cellphone_proc_action = QAction('新建手机视图', menu)
        add_cellphone_proc_action.triggered.connect(self.slot_add_cellphone_proc_view)
        menu.addAction(add_cellphone_proc_action)

        add_image_proc_action = QAction('添加图像处理视图', menu)
        add_image_proc_action.triggered.connect(self.slot_add_image_proc_view)
        menu.addAction(add_image_proc_action)

        add_multi_robots_action = QAction('添加多机器人控制器', menu)
        add_multi_robots_action.triggered.connect(self.slot_add_multi_robots_view)
        menu.addAction(add_multi_robots_action)

        add_EPuck_action = QAction('添加单个EPuck', menu)
        add_EPuck_action.triggered.connect(self.slot_add_EPuck)
        menu.addAction(add_EPuck_action)

        add_TPuck_action = QAction('添加单个TPuck', menu)
        add_TPuck_action.triggered.connect(self.slot_add_TPuck)
        menu.addAction(add_TPuck_action)

        add_VPuck_action = QAction('添加单个VPuck', menu)
        add_VPuck_action.triggered.connect(self.slot_add_VPuck)
        menu.addAction(add_VPuck_action)

        add_EPuck_test_action = QAction('添加EPuck测试', menu)
        add_EPuck_test_action.triggered.connect(self.slot_add_EPuck_test)
        menu.addAction(add_EPuck_test_action)

        clear_views_action = QAction('清空视图', menu)
        clear_views_action.triggered.connect(self.slot_clearSubview)
        menu.addAction(clear_views_action)
        return menu

    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(event.type(), ' ', QContextMenuEvent.MouseButtonRelease)
        # if event.type() == QContextMenuEvent.MouseButtonRelease:
        #     if event.button() == QtCore.Qt.RightButton:
        menu=self.mkQMenu()
        menu.exec_(event.globalPos())

    def getViewNameList(self):
        return [view.getDepict() for view in self.mViewList]
    
    def slot_add_cellphone_proc_view(self):
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250) 
        dialog.setWindowTitle('Set Input Cellphone')
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText('Input……（Cellphone\'s ip:port）')
        dialog.setTextValue('127.0.0.1:8881')
        dialog.setOkButtonText('Ok')
        dialog.setCancelButtonText('Cancel')
        if dialog.exec_() == QDialog.Accepted:
            dir = dialog.textValue()
            robot_controller = MainController.getController().mRobotController
            
            robot_controller.addRobot(RobotCellphone)
            robot = robot_controller.getRobot(-1)
            # robot:RobotVEpuck
            robot.setParent(self)
            robot.connect(dir)
            view = CellphoneFrame(self)
            view.setRobot(robot)
            self.addSubview(view)
        else:
            print("dialog canceled")
        dialog.show()

    def slot_add_multi_robots_view(self):
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250) 
        dialog.setWindowTitle('Set config file path')
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText('配置文件地址')
        dialog.setTextValue('./multi_robot_config.conf')
        dialog.setOkButtonText('Ok')
        dialog.setCancelButtonText('Cancel')
        if dialog.exec_() == QDialog.Accepted:
            config_path = dialog.textValue()
            view = MultiRobotControlFrame(self)
            view.loadConfigFile(config_path)
            self.addSubview(view)
        else:
            print("dialog canceled")
        dialog.show()

    def slot_add_VPuck(self):
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250) 
        dialog.setWindowTitle('Set Input Flow for Improcessor')
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText('请输入……（机器人的ip:port）')
        dialog.setTextValue('127.0.0.1:8881')
        dialog.setOkButtonText('Ok')
        dialog.setCancelButtonText('Cancel')
        if dialog.exec_() == QDialog.Accepted:
            dir = dialog.textValue()
            robot_controller = MainController.getController().mRobotController
            
            robot_controller.addRobot(RobotVEpuck)
            robot = robot_controller.getRobot(-1)
            # robot:RobotVEpuck
            robot.setParent(self)
            robot.connect(dir)
            view = RobotFrame(self)
            view.setRobot(robot)
            self.addSubview(view)
        else:
            print("dialog canceled")
        dialog.show()

    def slot_add_TPuck(self):
        pass

    def slot_add_EPuck(self):
        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setStyleSheet("""
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
        """)
        dialog.setFixedSize(350,250) 
        dialog.setWindowTitle('Set Input Flow for Improcessor')
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText('请输入……（机器人的ip）')
        dialog.setTextValue('192.168.3.5')
        dialog.setOkButtonText('Ok')
        dialog.setCancelButtonText('Cancel')
        if dialog.exec_() == QDialog.Accepted:
            ip = dialog.textValue()
            robot_controller = MainController.getController().mRobotController
            
            robot_controller.addRobot(RobotEpuck)
            robot = robot_controller.getRobot(-1)
            robot.connect(ip)
            view = RobotFrame(self)
            view.setRobot(robot)
            self.addSubview(view)
        else:
            print("dialog canceled")
        dialog.show()

    def slot_add_EPuck_test(self):
        robot_controller = MainController.getController().mRobotController
        robot_controller.addRobot(RobotEpuck)
        robot = robot_controller.getRobot(-1)
        view = RobotFrameTest(self)
        view.setRobot(robot)
        self.addSubview(view)

    def slot_add_image_proc_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        view = ImageProcViewFrame(self)
        self.addSubview(view)

    def on_add_camera_view(self, cam_id: int, cam_type: XCameraType):
        myDebug(self.__class__.__name__, get_current_function_name())
        camera_controller = MainController.getController().mCameraController
        camera = camera_controller.getCamera(cam_id)
        if camera and camera.isOpen():
            print('该相机已经打开')
        else:
            camera_controller.startCamera(cam_id, cam_type)
            view = CameraViewFrame(self)
            view.setCamera(camera_controller.mCameraList[len(camera_controller.mCameraList) - 1])
            self.addSubview(view)
            print('打开第%d个相机'%cam_id)

    def removeView(self, view):
        """
        将子视图从窗口中移除，不要调用removeWidget

        Args:
            view (_type_): 子视图
        """
        view.hide()
        self.mMainLayout.removeWidget(view)

    def addView(self, view, row, col):
        """
        窗口中添加子视图，不要调用addWidget

        Args:
            view (_type_): 子视图
            row (_type_): 子视图在窗口中排列的行号
            col (_type_): 子视图在窗口中排列的列号
        """
        view.show()
        self.mMainLayout.addWidget(view, row, col)

    def _multiLayout(self):
        """
        根据子图数量对子图进行排布
        """
        view_list_visible = self.getVisibleViewList()
        if len(view_list_visible) == 1:
            for widget in self.mViewList:
                self.removeView(widget)
            for widget in view_list_visible:
                self.addView(widget, 0, 0)
        elif len(view_list_visible) <= 4:
            for widget in self.mViewList:
                self.removeView(widget)
            for ind, widget in enumerate(view_list_visible):
                row = ind // 2
                col = ind % 2
                self.addView(widget, row, col)
        elif len(view_list_visible) <= 9:
            for widget in self.mViewList:
                self.removeView(widget)
            for ind, widget in enumerate(view_list_visible):
                row = ind // 3
                col = ind % 3
                self.addView(widget, row, col)
        elif len(view_list_visible) <= 16:
            for widget in self.mViewList:
                self.removeView(widget)
            for ind, widget in enumerate(view_list_visible):
                row = ind // 4
                col = ind % 4
                self.addView(widget, row, col)
        elif len(view_list_visible) <= 25:
            for widget in self.mViewList:
                self.removeView(widget)
            for ind, widget in enumerate(view_list_visible):
                row = ind // 5
                col = ind % 5
                self.addView(widget, row, col)
        elif len(view_list_visible) <= 36:
            for widget in self.mViewList:
                self.removeView(widget)
            for ind, widget in enumerate(view_list_visible):
                row = ind // 6
                col = ind % 6
                self.addView(widget, row, col)
                
    def reLayoutView(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        """
        mViewList重排
        """
        # print('test')
        if self.isViewMaximizedStateChanged:
            if self.mMaximizedView is None:
                self._multiLayout()
            else:
                for widget in self.mViewList:
                    self.removeView(widget)
                self.addView(self.mMaximizedView, 0, 0)
        else:
            if self.mMaximizedView is None:
                # self.mLastVisibleViewList = self.mViewList.copy()
                self._multiLayout()
            else:
                self.removeView(self.mMaximizedView)
                self.addView(self.mMaximizedView, 0, 0)
            

    def addSubview(self, view:ViewFrameBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        # self.mLastVisibleViewList = self.mViewList.copy()
        self.mViewList.append(view)
        view.signalDestroyed.connect(self.on_removeSubview)
        view.signalFocusedChanged.connect(self.slot_subview_active_changed)
        view.signalClearViews.connect(self.slot_clearSubview)
        view.signalAddImageProcView.connect(self.slot_add_image_proc_view)
        view.signalViewMaxmized.connect(self.slotMaximizeView)
        view.signalViewMinimized.connect(self.slotMinimizeView)
        view.signalVisibleChanged.connect(self.slot_subview_visible_changed)
        self.signalViewListChanged.emit()
        self.reLayoutView()

    def maximizeView(self, view:ViewFrameBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mMaximizedView is None:
            self.isViewMaximizedStateChanged = True
            # self.mLastVisibleViewList = self.mViewList.copy()
        else:
            self.isViewMaximizedStateChanged = False
            # self.mLastVisibleViewList = []
            # self.mLastVisibleViewList.append(self.mMaximizedView)
        self.setFocusedView(view)
        self.mMaximizedView = view
        self.reLayoutView()
        

    def minimizeView(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mMaximizedView is not None:
            self.isViewMaximizedStateChanged = True
            # self.mLastVisibleViewList = []
            # self.mLastVisibleViewList.append(self.mMaximizedView)
        else:
            self.isViewMaximizedStateChanged = False
        self.mMaximizedView = None
        self.reLayoutView()
        

    def encircleView(self, view:ViewFrameBase):
        """环绕显示，待实现
        """        
        myDebug(self.__class__.__name__, get_current_function_name())
        pass

    def slotMaximizeView(self, view:ViewFrameBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.maximizeView(view)
        self.signalViewShowStateChanged.emit(ViewShowState.viewMaximized)

    def slotMinimizeView(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.minimizeView()
        self.signalViewShowStateChanged.emit(ViewShowState.viewMinimized)

    def slotEncircleView(self, view:ViewFrameBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.encircleView(view)
        self.signalViewShowStateChanged.emit(ViewShowState.viewEncircled)

    def on_removeSubview(self, view):
        myDebug(self.__class__.__name__, get_current_function_name())
        if view.isFocused:
            self.setFocusedView(None)
        # visible_view_list = self.mViewList
        # self.mLastVisibleViewList = visible_view_list.copy()
        view_ind = self.mViewList.index(view)
        input_flow = self.mViewList[view_ind].getInputFlow()
        camera_controller = MainController.getController().mCameraController
        robot_controller = MainController.getController().mRobotController
        if type(input_flow) is CameraInterface:
            camera_controller.releaseCamera(input_flow.getID())
        elif type(input_flow) is RobotEpuck:
            robot_controller.releaseRobot(input_flow)
        self.mViewList.pop(self.mViewList.index(view))
        self.reLayoutView()

    def slot_subview_visible_changed(self):
        self.slotMinimizeView()
        self.signalViewListChanged.emit()
        # self.reLayoutView()

    def slot_subview_active_changed(self, view: ViewFrameBase, value: bool):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFocusedView:
            self.setFocusedView(None)
        if value:
            self.setFocusedView(view)
            # self.mFocusedView.active()
        else: 
            view.deactive()
        self.signalViewListChanged.emit()


    def slot_clearSubview(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        # self.mLastViewList = self.mViewList.copy()
        # self.mViewList = []
        # self.reLayoutView()
        camera_controller = MainController.getController().mCameraController
        for i in self.mViewList:
            i.destroy()
        self.mViewList = []
        camera_controller.releaseAllCamera()
        self.setFocusedView(None)
        self.reLayoutView()

    def setFocusedView(self, view):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFocusedView:
            self.mFocusedView.deactive()
            self.releaseKeyboard()
        self.mFocusedView = view
        if self.mFocusedView is not None:
            self.mFocusedView.active()
        if type(self.mFocusedView) is RobotFrame:
            self.grabKeyboard()
        
        self.signalViewFocusChanged.emit()
        

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        self.mBackgound.setGeometry(self.width()*0.5/3, self.height()*0.5/3, self.width()*2/3, self.height()*2/3)
        image = QPixmap("resource/images/earth.png")
        self.mBackgound.setPixmap(image.scaled(self.mBackgound.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.mFocusedView:
            if type(self.mFocusedView) is RobotFrame:
                self.mFocusedView.on_key_press(a0)

        # return super().keyPressEvent(a0)


def createInputDialog_robot():
    pass