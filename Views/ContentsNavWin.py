from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.uic import loadUi
from Views import WinBase, XLabel
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")


class ContentsNavWin(WinBase.WinBase):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(ContentsNavWin, self).__init__(*arg)
        loadUi('Views/ContentsNavWin.ui', self)

        self.id = 'ContentsNavWin'
        self.name = 'ContentsNavWin'

        self.mkConnect()

    def mkConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.btnToTestForm: QPushButton
        self.btnToTestForm.clicked.connect(self.on_btnToTestForm)
        self.btnToMVForm.clicked.connect(self.on_btnToMVForm)

    def on_btnToTestForm(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.signalChangeWin.emit('TestCameraWin')

    def on_btnToMVForm(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        # self.signalChangeWin
        pass