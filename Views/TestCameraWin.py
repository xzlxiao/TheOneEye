from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QGridLayout
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.uic import loadUi
from Views import WinBase, XLabel
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")


class TestCameraWin(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(TestCameraWin, self).__init__(*arg)
        loadUi('Views/TestCameraWin2.ui', self)

        self.lbCameraShow: QLabel
        self.mCameraShow = XLabel.XLabel(self)

        self.mainlayout1.replaceWidget(self.lbCameraShow, self.mCameraShow)
        self.lbCameraShow.hide()
        self.mCameraShow.setStyleSheet("background-color: rgb(114, 159, 200);")
        self.mCameraShow.show()

        self.id = 'TestCameraWin'
        self.name = 'TestCameraWin'
