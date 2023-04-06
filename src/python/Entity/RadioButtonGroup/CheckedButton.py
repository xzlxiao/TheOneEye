from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QListView
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QStringListModel, QEvent, Qt
from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie, QMouseEvent
from Common.Common import Common

class CheckedButton(QWidget):
    signalButtonActived = pyqtSignal()
    signalButtonDeactived = pyqtSignal()
    def __init__(self, button:QLabel, parent=None, isChecked=False, image_normal=None, image_hover=None, image_press=None, image_active=None) -> None:
        """自制radio buton

        Args:
            button (QLabel): 基础控件
            image_normal (): 未点击时显示的图像
            image_hover (): 鼠标悬浮时的图像
            image_press (): 按下鼠标时的图像
            image_active (): 激活时的图像
        """        
        super().__init__(parent)
        self.mImage_normal = None           # 未点击时显示的图像
        self.mImage_hover = None    # 鼠标悬浮时的图像
        self.mImage_press = None    # 按下鼠标时的图像
        self.mImage_active = None   # 激活时的图像

        if image_normal is None:
            self.mImage_normal = 'resource/icons/fault.png'
        else:
            self.mImage_normal = image_normal  

        if image_hover is None:
            if image_normal is None:
                self.mImage_hover = 'resource/icons/fault.png'
            else:
                self.mImage_hover = image_normal
        else:
            self.mImage_hover = image_hover
        
        if image_press is None:
            if image_normal is None:
                self.mImage_press = 'resource/icons/fault.png'
            else:
                self.mImage_press = image_normal
        else:
            self.mImage_press = image_press
        
        if image_active is None:
            if image_normal is None:
                self.mImage_active = 'resource/icons/fault.png'
            else:
                self.mImage_active = image_normal
        else:
            self.mImage_active = image_active
        
        self.mButton = button         # 实际的控件，QLabel
        self.mButton.installEventFilter(self)       # 事件过滤器

        self.__isActived = False     # 是否激活
        if isChecked:
            self.active()
        else:
            self.deactive()

        

    def active(self):
        self.__isActived = True 
        Common.setQLabelImage(self.mImage_active, self.mButton)
        self.update()

    def deactive(self):
        self.__isActived = False 
        Common.setQLabelImage(self.mImage_normal, self.mButton)
        self.update()
    
    def update(self):
        self.mButton.update()

    def isActived(self):
        return self.__isActived


    def eventFilter(self, watched: QObject, e: QEvent) -> bool:
        # super().eventFilter(a0, a1)
        isEventGot = False
        if watched is self.mButton:
            
            if e.type() == QMouseEvent.Enter:
                if not self.isActived():
                    
                    Common.setQLabelImage(self.mImage_hover, self.mButton)
                    isEventGot = True
            elif e.type() == QMouseEvent.Leave:
                if not self.isActived():
                    Common.setQLabelImage(self.mImage_normal, self.mButton)
                    isEventGot = True
            elif e.type() == QMouseEvent.MouseButtonPress:
                if e.button() == Qt.LeftButton:
                    Common.setQLabelImage(self.mImage_press, self.mButton)
                    isEventGot = True
            elif e.type() == QMouseEvent.MouseButtonRelease:
                if self.isActived():
                    self.deactive()
                    # Common.setQLabelImage(self.mImage_normal, self.mButton)
                    self.signalButtonDeactived.emit()
                    isEventGot = True
                else:
                    self.active()
                    
                    self.signalButtonActived.emit()
                    isEventGot = True
            self.update()
        return isEventGot

    
