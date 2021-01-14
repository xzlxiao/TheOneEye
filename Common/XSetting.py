from Common.DebugPrint import myDebug, get_current_function_name, DebugPrint
import sys
sys.path.append("../")
import os

from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject, QEvent, QCoreApplication, QSettings
from PyQt5.uic import loadUi
from Views import WinBase, XLabel


class XSetting(QObject):
    mName = 'None'
    isDebug = DebugPrint
    isShowBorder = False
    isCameraDebug = False

    def __init__(self, *args):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(XSetting, self).__init__(*args)

    @staticmethod
    def print():
        myDebug(XSetting.__class__.__name__, get_current_function_name())
        print("【XSetting test】")
        print("Test/Name: {}".format(XSetting.mName))

    @staticmethod
    def setValue(key: str, value: str):
        myDebug(XSetting.__class__.__name__, get_current_function_name())
        ConfigFileDir = "Config.ini"
        my_setting = QSettings(ConfigFileDir, QSettings.IniFormat)
        my_setting.setValue(key, value)

    @staticmethod
    def getValue(key: str) -> str:
        myDebug(XSetting.__class__.__name__, get_current_function_name())
        ConfigFileDir = "Config.ini"
        my_setting = QSettings(ConfigFileDir, QSettings.IniFormat)
        return my_setting.value(key, "Fail", type=str)

    @staticmethod
    def removeValue(key: str):
        myDebug(XSetting.__class__.__name__, get_current_function_name())
        ConfigFileDir = "Config.ini"
        my_setting = QSettings(ConfigFileDir, QSettings.IniFormat)
        my_setting.remove(key)

    @staticmethod
    def loadSettingFile():
        myDebug(XSetting.__class__.__name__, get_current_function_name())
        ConfigFileDir = "Config.ini"
        my_setting = QSettings(ConfigFileDir, QSettings.IniFormat)
        XSetting.mName = my_setting.value("Test/Name", "Fail", type=str)
        DebugPrint.isPrintDebug = my_setting.value("Debug/isDebug", False, type=bool)
        print(DebugPrint.isPrintDebug)
        print(XSetting.isDebug.isPrintDebug)
        XSetting.isShowBorder = my_setting.value("Debug/isShowBorder", False, type=bool)
        XSetting.isCameraDebug = my_setting.value("Debug/isCameraDebug", False, type=bool)
