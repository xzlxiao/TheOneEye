from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QSizePolicy, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
from Views.ViewFrameBase import ViewFrameBase
import PyQt5

class CameraViewFrame(ViewFrameBase):
    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(CameraViewFrame, self).__init__(*args)
        self.mLayout = QVBoxLayout(self)
        self.mLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mLayout)
        self.mCameraNameLabel = QLabel(self)
        self.mCameraNameLabel.setFixedHeight(20)
        self.mCameraNameLabel.setStyleSheet("color: rgb(255, 0, 0);border:0px solid rgba(100, 100, 100, 0);")
        self.mCameraNameLabel.show()
        self.mCamera = None
        self.foot_label = QLabel(self)
        self.foot_label.setFixedHeight(20)
        self.foot_label.setStyleSheet("color: rgb(255, 0, 0);border:0px solid rgba(100, 100, 100, 0);")
        self.foot_label.show()


    def setCamera(self, camera):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mOptionList = []
        camera_name = "unknown"
        if camera.mCameraName:
            camera_name = camera.mCameraName
        self.mCameraNameLabel.setText(camera_name)
        self.mCamera = camera
        self.mLayout.addWidget(self.mCameraNameLabel)
        self.mLayout.addWidget(camera.mViewCamera)
        self.mLayout.addWidget(self.foot_label)
        self.insertOptionList(camera_name, self.defaultFunc)
        self.insertOptionList('This is Camera View', self.defaultFunc)
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        # print(event.type(), ' ', QContextMenuEvent.MouseButtonRelease)
        # if event.type() == QContextMenuEvent.MouseButtonRelease:
        #     if event.button() == QtCore.Qt.RightButton:
        menu=self.mkQMenu()
        menu.exec_(event.globalPos())

    def getInputFlow(self):
        return self.mCamera