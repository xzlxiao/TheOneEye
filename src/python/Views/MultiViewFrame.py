from functools import partial

import PyQt5
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QSizePolicy, QVBoxLayout, QListView
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Entity.CameraInterface import CameraInterface
from Views.CameraViewFrame import CameraViewFrame
from Views.ImageProcViewFrame import ImageProcViewFrame
from Views.ViewFrameBase import ViewFrameBase
from Control.CameraController import XCameraType
import copy

class MultiViewFrame(QFrame):
    signalViewFocusChanged = pyqtSignal()
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
        self.mLastViewList = []
        self.mViewList = []
        self.mCameregister = []
        self.mCameregister.append(self.on_add_camera0_view)
        self.mCameregister.append(self.on_add_camera1_view)
        self.mCameregister.append(self.on_add_camera2_view)
        self.mCameregister.append(self.on_add_camera3_view)
        self.mCameregister.append(self.on_add_camera4_view)

    def mkQMenu(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        menu=QMenu(self)
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

        add_image_proc_action = QAction('添加图像处理视图', menu)
        add_image_proc_action.triggered.connect(self.slot_add_image_proc_view)
        menu.addAction(add_image_proc_action)

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

    def on_add_camera0_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        camera_controller = MainController.getController().mCameraController
        camera = camera_controller.getCamera(0)
        if camera and camera.isOpen():
            print('该相机已经打开')
        else:
            camera_controller.startCamera(0)
            view = CameraViewFrame(self)
            view.setCamera(camera_controller.mCameraList[len(camera_controller.mCameraList)-1])
            self.addSubview(view)
            print('打开第0个相机')

    def on_add_camera1_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        camera_controller = MainController.getController().mCameraController
        camera = camera_controller.getCamera(0)
        if camera and camera.isOpen():
            print('该相机已经打开')
        else:
            camera_controller.startCamera(1)
            view = CameraViewFrame(self)
            view.setCamera(camera_controller.mCameraList[len(camera_controller.mCameraList)-1])
            self.addSubview(view)
            print('打开第1个相机')

    def on_add_camera2_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        camera_controller = MainController.getController().mCameraController
        camera = camera_controller.getCamera(0)
        if camera and camera.isOpen():
            print('该相机已经打开')
        else:
            camera_controller.startCamera(2)
            view = CameraViewFrame(self)
            view.setCamera(camera_controller.mCameraList[len(camera_controller.mCameraList)-1])
            self.addSubview(view)
            print('打开第2个相机')

    def on_add_camera3_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        camera_controller = MainController.getController().mCameraController
        camera = camera_controller.getCamera(0)
        if camera and camera.isOpen():
            print('该相机已经打开')
        else:
            camera_controller.startCamera(3)
            view = CameraViewFrame(self)
            view.setCamera(camera_controller.mCameraList[len(camera_controller.mCameraList)-1])
            self.addSubview(view)
            print('打开第3个相机')

    def on_add_camera4_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        camera_controller = MainController.getController().mCameraController
        camera = camera_controller.getCamera(0)
        if camera and camera.isOpen():
            print('该相机已经打开')
        else:
            camera_controller.startCamera(4)
            view = CameraViewFrame(self)
            view.setCamera(camera_controller.mCameraList[len(camera_controller.mCameraList)-1])
            self.addSubview(view)
            print('打开第4个相机')

    def reLayoutView(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        """
        mViewList重排
        """
        # print('test')
        if len(self.mViewList) == 1:
            for widget in self.mLastViewList:
                self.mMainLayout.removeWidget(widget)
            for widget in self.mViewList:
                self.mMainLayout.addWidget(widget, 0, 0, 1, 1)
        elif len(self.mViewList) <= 4:
            for widget in self.mLastViewList:
                self.mMainLayout.removeWidget(widget)
            for ind, widget in enumerate(self.mViewList):
                row = ind // 2
                col = ind % 2
                self.mMainLayout.addWidget(widget, row, col, 1, 1)
        elif len(self.mViewList) <= 9:
            for widget in self.mLastViewList:
                self.mMainLayout.removeWidget(widget)
            for ind, widget in enumerate(self.mViewList):
                row = ind // 3
                col = ind % 3
                self.mMainLayout.addWidget(widget, row, col, 1, 1)
        elif len(self.mViewList) <= 16:
            for widget in self.mLastViewList:
                self.mMainLayout.removeWidget(widget)
            for ind, widget in enumerate(self.mViewList):
                row = ind // 4
                col = ind % 4
                self.mMainLayout.addWidget(widget, row, col, 1, 1)
        elif len(self.mViewList) <= 25:
            for widget in self.mLastViewList:
                self.mMainLayout.removeWidget(widget)
            for ind, widget in enumerate(self.mViewList):
                row = ind // 5
                col = ind % 5
                self.mMainLayout.addWidget(widget, row, col, 1, 1)
        elif len(self.mViewList) <= 36:
            for widget in self.mLastViewList:
                self.mMainLayout.removeWidget(widget)
            for ind, widget in enumerate(self.mViewList):
                row = ind // 6
                col = ind % 6
                self.mMainLayout.addWidget(widget, row, col, 1, 1)

    def addSubview(self, view:ViewFrameBase):
        myDebug(self.__class__.__name__, get_current_function_name())
        if len(self.mViewList) < 36:
            self.mLastViewList = self.mViewList.copy()
            self.mViewList.append(view)
            view.signalDestroyed.connect(self.on_removeSubview)
            view.signalFocusedChanged.connect(self.slot_subview_active_changed)
            view.signalClearViews.connect(self.slot_clearSubview)
            view.signalAddImageProcView.connect(self.slot_add_image_proc_view)
            self.reLayoutView()
            
        
    def on_removeSubview(self, view):
        myDebug(self.__class__.__name__, get_current_function_name())
        if view.isFocused:
            self.setFocusedView(None)
        self.mLastViewList = self.mViewList.copy()
        view_ind = self.mViewList.index(view)
        input_flow = self.mViewList[view_ind].getInputFlow()
        camera_controller = MainController.getController().mCameraController
        if type(input_flow) is CameraInterface:
            camera_controller.releaseCamera(input_flow.getID())
        self.mViewList.pop(self.mViewList.index(view))
        self.reLayoutView()

    def slot_subview_active_changed(self, view: ViewFrameBase, value: bool):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFocusedView:
            self.setFocusedView(None)
        if value:
            self.setFocusedView(view)
            self.mFocusedView.active()
        else: 
            view.deactive()


    def slot_clearSubview(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mLastViewList = self.mViewList.copy()
        self.mViewList = []
        self.reLayoutView()
        camera_controller = MainController.getController().mCameraController
        for i in self.mLastViewList:
            i.destroy()
        camera_controller.releaseAllCamera()
        self.setFocusedView(None)

    def setFocusedView(self, view):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFocusedView:
            self.mFocusedView.deactive()
        self.mFocusedView = view
        self.signalViewFocusChanged.emit()
        

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        self.mBackgound.setGeometry(self.width()*0.5/3, self.height()*0.5/3, self.width()*2/3, self.height()*2/3)
        image = QPixmap("resource/images/earth.png")
        self.mBackgound.setPixmap(image.scaled(self.mBackgound.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
