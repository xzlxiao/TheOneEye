from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QObject
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

class WinBase(QtWidgets.QWidget):
    def __init__(self, *args):
        print("%s.%s invoked" % (self.__class__.__name__, get_current_function_name()))
        super(WinBase, self).__init__(*args)
        self.id: str
        self.name: str
        self.signalReturn = pyqtSignal()

    def windowLoad(self):
        print("%s.%s invoked" % (self.__class__.__name__, get_current_function_name()))
        pass

