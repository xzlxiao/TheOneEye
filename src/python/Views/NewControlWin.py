"""
       .==.        .==.
      //`^\\      //^`\\
     // ^ ^\(\__/)/^ ^^\\
    //^ ^^ ^/+  0\ ^^ ^ \\
   //^ ^^ ^/( >< )\^ ^ ^ \\
  // ^^ ^/\| v''v |/\^ ^ ^\\
 // ^^/\/ /  `~~`  \ \/\^ ^\\
 ----------------------------
BE CAREFULL! THERE IS A DRAGON.

Function：NewControlWin

Modules：
pass

(c) 肖镇龙(xzl) 2023

"""
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QListView, QTreeView
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QStringListModel, Qt, QTimer
from PyQt5.QtGui import QResizeEvent, QPixmap, QMovie, QStandardItemModel, QStandardItem

from PyQt5.uic import loadUi
from Views import WinBase, MultiViewFrame, HomePage, SettingPage
from Common.Common import Common
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
from Common.WindowSwitcher import WindowSwitcher
from Control import MainController
from Entity.RadioButtonGroup.RadioButtonGroup import RadioButtonGroup
from Entity.RadioButtonGroup.RadioButton import RadioButton
from Entity.ViewListQItem import ViewListQItem
import sys
sys.path.append("../")

class NewControlWin(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(NewControlWin, self).__init__(*arg)
        loadUi(XSetting.getValue('Python/SrcDir')+'Views/NewControlWin.ui', self)

        self.id = 'NewControlWin'
        self.name = 'NewControlWin'

        self.isStartBackMovie = False

        Common.setQLabelImage('resource/icons/Logo2.png', self.labelLogo)
        Common.setQLabelImage('resource/icons/time.png', self.labelTimeIcon)
        Common.setQLabelImage('resource/icons/date.png', self.labelDateIcon)
        self.labelTimeIcon.setStyleSheet('')
        self.labelDateIcon.setStyleSheet('')
        self.mTimeUpdate_timer = QTimer()
        self.mTimeUpdate_timer.setInterval(1000)
        self.mPageGroup = RadioButtonGroup(self)
        
        home_page_img_normal = 'resource/icons/home_normal.png'
        home_page_img_hover = 'resource/icons/home_hover.png'
        home_page_img_press = 'resource/icons/home_press.png'
        home_page_img_active = 'resource/icons/home_active.png'
        self.btnHome.setStyleSheet('')
        self.mPageGroup.addButton(
            'HomePage', 
            self.btnHome, 
            isActived=True, 
            image_active=home_page_img_active,
            image_hover=home_page_img_hover,
            image_normal=home_page_img_normal,
            image_press=home_page_img_press)
        
        setting_page_img_normal = 'resource/icons/setting_normal.png'
        setting_page_img_hover = 'resource/icons/setting_hover.png'
        setting_page_img_press = 'resource/icons/setting_press.png'
        setting_page_img_active = 'resource/icons/setting_active.png'
        self.btnSetting.setStyleSheet('')
        self.mPageGroup.addButton(
            'SettingPage',
            self.btnSetting,
            isActived=False,
            image_active=setting_page_img_active,
            image_hover=setting_page_img_hover,
            image_normal=setting_page_img_normal,
            image_press=setting_page_img_press
        )
        self.mHomePage = HomePage.HomePage(self)
        self.mHomePage.hide()
        self.mSettingPage = SettingPage.SettingPage(self)
        self.mSettingPage.hide()
        self.mPageLayout = QGridLayout(self.mainFrame)
        self.mFrameViewArea = self.mHomePage.mFrameViewArea.mFrameViewArea
        self.mPageSwitcher = WindowSwitcher()
        self.mPageSwitcher.setMainLayout(self.mPageLayout)
        self.mPageSwitcher.switchTo(self.mHomePage)

        self.__DevicesModel = QStandardItemModel(self)
        
        self.__DevicesModel.setHorizontalHeaderLabels(('设备',))
        self.treeViewDeviceList: QTreeView
        self.treeViewDeviceList.setModel(self.__DevicesModel)
        self.treeViewDeviceList.expandAll()


        
        self.mkConnect()
        self.mTimeUpdate_timer.start()

    def getViewNameList(self):
        return self.mHomePage.getViewNameList()
    
    def getMultiViewFrame(self):
        return self.mHomePage.mFrameViewArea.mFrameViewArea
    
    def mkConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.btnReturn.clicked.connect(self.on_ReturnButton)
        self.btnReturn.clicked.connect(self.slot_return)
        self.mTimeUpdate_timer.timeout.connect(self.on_time_update)
        self.mPageGroup.getButton('HomePage').signalButtonActived.connect(self.on_home_page_actived)
        self.mPageGroup.getButton('SettingPage').signalButtonActived.connect(self.on_setting_page_actived)
        self.getMultiViewFrame().signalViewListChanged.connect(self.slot_view_list_changed)

    def updateDeviceList(self):
        model = self.getDevicesModel()
        item_camera = QStandardItem('相机')
        item_camera.setEditable(False)
        model.setItem(0, 0, item_camera)
        controller = MainController.getController()
        camera_list, _ = controller.mCameraController.getAvailableCameraNames()
        for ind, name in enumerate(camera_list):
            item = QStandardItem(name)
            item.setEditable(False)
            item_camera.setChild(ind, 0, item)

        item_view = QStandardItem('视图')
        item_view.setEditable(False)
        model.setItem(1, 0, item_view)
        view_depict_list = self.getViewNameList()
        for ind, depict in enumerate(view_depict_list):
            item = ViewListQItem(depict)
            item_view.setChild(ind, 0, item)
        self.treeViewDeviceList.expandAll()

    def getDevicesModel(self):
        return self.__DevicesModel

    def showEvent(self, event):
        self.setReturnButtonLoc()
        self.updateDeviceList()
        # view_size = self.width()/4
        # self.lbViewState.setMaximumSize(view_size, view_size)

    def hideEvent(self, event):
        pass


    def slot_return(self):
        myDebug(self.__class__.__name__, get_current_function_name())
    # def setReturnButtonLoc(self):
    #     self.mReturnButton.move(self.width() / 10, self.height() * 8 / 10)

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)

    def on_time_update(self):
        time1 = Common.getTime(r"%H:%M:%S")
        date1 = Common.getTime(r"%Y-%m-%d")
        self.labelDate:QLabel
        self.labelTime:QLabel
        self.labelDate.setText(date1)
        self.labelTime.setText(time1)

    def on_home_page_actived(self, name):
        print(name)
        self.mPageSwitcher.switchTo(self.mHomePage)

    def on_setting_page_actived(self, name):
        print(name)
        self.mPageSwitcher.switchTo(self.mSettingPage)

    def slot_view_list_changed(self):
        self.updateDeviceList()