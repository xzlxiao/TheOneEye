from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QListView, QSizePolicy, QTreeView
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QStringListModel, QEvent, Qt, QSize
from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie, QMouseEvent, QIcon, QStandardItemModel, QStandardItem

from PyQt5.uic import loadUi
from Views import WinBase, MultiViewFrame
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
from Control import MainController
from Entity.RadioButtonGroup.CheckedButton import CheckedButton
from Entity.RadioButtonGroup.RadioButtonGroup import RadioButtonGroup
import sys
sys.path.append("../")

class HomePageMainView(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(HomePageMainView, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/HomePageMainView.ui', self)

        self.id = 'HomePageMainView'
        self.name = 'HomePageMainView'
   
        self.mFrameViewArea = MultiViewFrame.MultiViewFrame(self)
        # self.mFrameViewArea.setStyleSheet('')

        self.verticalLayoutViews.replaceWidget(self.frameViewArea, self.mFrameViewArea)
        self.mFrameViewArea.show()
        self.mFrameViewArea.setMinimumSize(0, 0)
        self.mFrameViewArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        
        self.frameViewArea.hide()
        self.frameViewArea.destroy()

        self.mSlm = QStringListModel()
        self.listViewOption.setModel(self.mSlm)

        movie = QMovie("resource/images/AI.gif")
        # self.mImage_viewState = QPixmap()
        # self.mImage_viewState.load('resource/images/Grid4.png')
        
        # self.lbViewState.setAlignment(QtCore.Qt.AlignCenter)
        # self.lbViewState.setMovie(movie)
        # self.lbViewState.setScaledContents(True)
        # view_size = self.width()/4
        # self.lbViewState.setMaximumSize(view_size, view_size)
        # self.lbViewState.setMaximumWidth(view_size)
        # movie.start()
        icon_dir = XSetting.getValue('Python/ResourceDir')+'icons/'
        self.mBtnViewOption = CheckedButton(
            self.btnViewOption, 
            self, 
            True, 
            icon_dir+'con_option_normal.png',
            icon_dir+'con_option_hover.png',
            icon_dir+'con_option_press.png',
            icon_dir+'con_option_active.png')
        self.frameViewOption.show()

        self.mBtnViewPanel = CheckedButton(
            self.btnViewPanel, 
            self, 
            False, 
            icon_dir+'con_panel_normal.png',
            icon_dir+'con_panel_hover.png',
            icon_dir+'con_panel_press.png',
            icon_dir+'con_panel_active.png')
        self.frameViewPanel.hide()

        self.mBtnViewState = CheckedButton(
            self.btnViewState, 
            self, 
            False, 
            icon_dir+'con_state_normal.png',
            icon_dir+'con_state_hover.png',
            icon_dir+'con_state_press.png',
            icon_dir+'con_state_active.png')
        self.frameViewState.hide()
        self.mShowStateButtonGroup = RadioButtonGroup()
        self.mShowStateButtonGroup.addButton(
            'view_full',
            self.labelFullShow, 
            False, 
            icon_dir+'view_full_normal.png',
            icon_dir+'view_full_hover.png',
            icon_dir+'view_full_press.png',
            icon_dir+'view_full_active.png'
        )

        self.mShowStateButtonGroup.addButton(
            'view_equal',
            self.labelEqualShow, 
            True, 
            icon_dir+'view_equal_normal.png',
            icon_dir+'view_equal_hover.png',
            icon_dir+'view_equal_press.png',
            icon_dir+'view_equal_active.png'
        )

        self.mShowStateButtonGroup.addButton(
            'view_encircle',
            self.labelEncircleShow, 
            False, 
            icon_dir+'view_focus_normal.png',
            icon_dir+'view_focus_hover.png',
            icon_dir+'view_focus_press.png',
            icon_dir+'view_focus_active.png'
        )

        

        self.mkConnect()

        # self.eventFilterInstall()

    # def eventFilterInstall(self):
    #     self.btnViewOption.installEventFilter(self)
    #     self.btnViewPanel.installEventFilter(self)
    #     self.btnViewState.installEventFilter(self)

    def getViewNameList(self):
        return self.mFrameViewArea.getViewNameList()

    def mkConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mFrameViewArea.signalViewFocusChanged.connect(self.slot_view_focus_changed)
        self.listViewOption.clicked.connect(self.on_clicked_list)
        self.mBtnViewOption.signalButtonActived.connect(self.on_BtnViewOption_actived)
        self.mBtnViewOption.signalButtonDeactived.connect(self.on_BtnViewOption_deactived)
        self.mBtnViewPanel.signalButtonActived.connect(self.on_BtnViewPanel_actived)
        self.mBtnViewPanel.signalButtonDeactived.connect(self.on_BtnViewPanel_deactived)
        self.mBtnViewState.signalButtonActived.connect(self.on_BtnViewState_actived)
        self.mBtnViewState.signalButtonDeactived.connect(self.on_BtnViewstate_deactived)
        self.mShowStateButtonGroup.getButton('view_full').signalButtonActived.connect(self.on_BtnViewFull_actived)
        self.mShowStateButtonGroup.getButton('view_equal').signalButtonActived.connect(self.on_BtnViewEqual_actived)
        self.mShowStateButtonGroup.getButton('view_encircle').signalButtonActived.connect(self.on_BtnViewEncircle_actived)
        self.mFrameViewArea.signalViewShowStateChanged.connect(self.on_view_show_state_changed)

    def showEvent(self, event):
        pass
        # view_size = self.width()/4
        # self.lbViewState.setMaximumSize(view_size, view_size)

    def hideEvent(self, event):
        pass

    

    def slot_view_focus_changed(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFrameViewArea.mFocusedView:
            self.mSlm.setStringList(self.mFrameViewArea.mFocusedView.mOptionList)
        else:
            self.mSlm.setStringList([])

    def on_clicked_list(self, qModelIndex):
        myDebug(self.__class__.__name__, get_current_function_name())
        if self.mFrameViewArea.mFocusedView:
            self.mFrameViewArea.mFocusedView.mOptionFuncList[qModelIndex.row()](qModelIndex.row())

    def on_BtnViewOption_actived(self):
        self.frameViewOption.show()

    def on_BtnViewOption_deactived(self):
        self.frameViewOption.hide()

    def on_BtnViewPanel_actived(self):
        self.frameViewPanel.show()

    def on_BtnViewPanel_deactived(self):
        self.frameViewPanel.hide()

    def on_BtnViewState_actived(self):
       self.frameViewState.show()

    def on_BtnViewstate_deactived(self):
        self.frameViewState.hide()

    def on_BtnViewFull_actived(self):
        if self.mFrameViewArea.mFocusedView is not None:
            self.mFrameViewArea.maximizeView(self.mFrameViewArea.mFocusedView)
        elif len(self.mFrameViewArea.mViewList)>0:
            self.mFrameViewArea.maximizeView(self.mFrameViewArea.mViewList[0])

    def on_BtnViewEqual_actived(self):
        self.mFrameViewArea.minimizeView() 

    def on_BtnViewEncircle_actived(self):
        pass 

    def on_view_show_state_changed(self, state: MultiViewFrame.ViewShowState):
        if state == MultiViewFrame.ViewShowState.viewMaximized:
            self.mShowStateButtonGroup.activeButton('view_full')
        elif state == MultiViewFrame.ViewShowState.viewMinimized:
            self.mShowStateButtonGroup.activeButton('view_equal') 
        elif state == MultiViewFrame.ViewShowState.viewEncircled:
            self.mShowStateButtonGroup.activeButton('view_encircle')

    # def eventFilter(self, a0: 'QObject', a1: 'QEvent'):
    #     ret = super().eventFilter(a0, a1)

    #     if a0 == self.btnViewOption:
    #         self.__buttonIconConfig(a0, a1, 'con_option_normal.png', 'con_option_hover.png', 'con_option_press.png', 'con_option_active.png') 
    #         ret = True
    #     elif a0 == self.btnViewPanel:
    #         self.__buttonIconConfig(a0, a1, 'con_panel_normal.png', 'con_panel_hover.png', 'con_panel_press.png', 'con_panel_active.png') 
    #         ret = True
    #     elif a0 == self.btnViewState:
    #         self.__buttonIconConfig(a0, a1, 'con_state_normal.png', 'con_state_hover.png', 'con_state_press.png', 'con_state_active.png') 
    #         ret = True
    #     return ret

    # def __buttonIconConfig(self, btn: QLabel, e: QEvent, image_normal_filename:str, image_hover_filename:str, image_press_filename:str, image_active_filename:str)->None:
    #     """用来处理按钮的状态变化事件，注：地址只写文件名，文件放在Resource/icons文件夹里

    #     Args:
    #         btn (QPushButton): 按钮
    #         e (QEvent): 事件
    #         image_normal_filename (str): 普通状态的icon文件名
    #         image_hover_filename (str): 鼠标悬停状态的icon文件名
    #         image_press_filename (str): 鼠标按压状态的icon文件名
    #         image_active_filename (str): 激活状态的icon文件名
    #     """        
    #     if e.type() == QMouseEvent.Enter:
    #         if not btn.isChecked():
    #             icon = QIcon()
    #             icon.addFile(XSetting.getValue('Python/ResourceDir')+'icons/'+image_hover_filename)
    #             print(icon.pixmap())
    #             btn.setIcon(icon)
    #     elif e.type() == QMouseEvent.Leave:
    #         if not btn.isChecked():
    #             icon = QIcon(XSetting.getValue('Python/ResourceDir')+'icons/'+image_normal_filename)
    #             btn.setIcon(icon)
    #     elif e.type() == QMouseEvent.MouseButtonPress:
    #         if e.button() == Qt.LeftButton:
    #             icon = QIcon(XSetting.getValue('Python/ResourceDir')+'icons/'+image_press_filename)
    #             btn.setIcon(icon)
    #     elif e.type() == QMouseEvent.MouseButtonRelease:
    #         if btn.isChecked():
    #             icon = QIcon(XSetting.getValue('Python/ResourceDir')+'icons/'+image_active_filename)
    #             btn.setIcon(icon)
    #         else:
    #             icon = QIcon(XSetting.getValue('Python/ResourceDir')+'icons/'+image_normal_filename)
    #             btn.setIcon(icon)
    #     btn.update()

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        # view_size = self.width()/4
        # self.lbViewState.setMaximumSize(view_size, view_size)