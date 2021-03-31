from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QSizePolicy, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui, uic, QtMultimediaWidgets
from PyQt5.QtGui import QContextMenuEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import pyqtSignal, QObject, QSize, QEvent
from Control import MainController
from Common.DebugPrint import myDebug, get_current_function_name
import PyQt5


class ViewFrameBase(QFrame):
    signalDestroyed = pyqtSignal(QFrame)
    signalFocusedChanged = pyqtSignal(QFrame, bool)
    signalClearViews = pyqtSignal()
    signalAddImageProcView = pyqtSignal()
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(ViewFrameBase, self).__init__(*arg)
        self.mActiveBorderStyle = 'border:2px solid rgba(200, 50, 50, 255);'
        self.mUnactiveBorderStyle = 'border:2px solid rgba(200, 200, 200, 150);'
        self.deactive()
        self.isFocused = False
        self.mOptionList = []
        self.mOptionFuncList = []
    
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        myDebug(self.__class__.__name__, get_current_function_name())
        super().mouseReleaseEvent(a0)
        if self.isFocused:
            self.signalFocusedChanged.emit(self, False)
        else: 
            self.signalFocusedChanged.emit(self, True)
        

    def active(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.isFocused = True
        self.setStyleSheet(self.mActiveBorderStyle)

    def deactive(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.isFocused = False
        self.setStyleSheet(self.mUnactiveBorderStyle)

    def on_del_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.destroy()
        self.signalDestroyed.emit(self)

    def on_clear_views(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.signalClearViews.emit()

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
        camera_names = controller.mCameraController.getAvailableCameraNames()
        for ind, name in enumerate(camera_names):
            cam_action = QAction(name, camera_list)
            if self.parent():
                cam_action.triggered.connect(self.parent().mCameregister[ind])
            camera_list.addAction(cam_action)
        menu.addMenu(camera_list)

        add_image_proc_action = QAction('添加图像处理视图', menu)
        add_image_proc_action.triggered.connect(self.slot_add_image_proc_view)
        menu.addAction(add_image_proc_action)

        del_view_action = QAction('删除视图', menu)
        del_view_action.triggered.connect(self.on_del_view)
        clear_view_action = QAction('清空视图', menu)
        clear_view_action.triggered.connect(self.on_clear_views)
        menu.addAction(del_view_action)
        menu.addAction(clear_view_action)
        return menu

    def slot_add_image_proc_view(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.signalAddImageProcView.emit()

    def insertOptionList(self, name, func, insert_ind=-1):
        myDebug(self.__class__.__name__, get_current_function_name())
        if insert_ind == -1 or len(self.mOptionList)==0:
            self.mOptionList.append(name)
            self.mOptionFuncList.append(func)
        elif insert_ind >= 0 and insert_ind < len(self.mOptionList):
            self.mOptionList.insert(insert_ind, name)
            self.mOptionFuncList.insert(insert_ind, func)
        else: 
            raise IndexError()

    def deleteOptionList(self, ind):
        myDebug(self.__class__.__name__, get_current_function_name())
        if ind >= 0 and ind < len(self.mOptionList):
            self.mOptionList.pop(ind)
            self.mOptionFuncList.pop(ind)
        else:
            raise IndexError()
    
    def clearOptionList(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mOptionList.clear()
        self.mOptionFuncList.clear()

    def defaultFunc(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        print('defaultFunc')

    def getOptionListLen(self):
        return len(self.mOptionList)

    def getInputFlow(self):
        return None