from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

class WinBase(QtWidgets.QWidget):
    signalReturn = pyqtSignal()
    signalChangeWin = pyqtSignal(str)
    def __init__(self, *args):
        super(WinBase, self).__init__(*args)
        self.id: str
        self.name: str

    def windowLoad(self):
        pass

