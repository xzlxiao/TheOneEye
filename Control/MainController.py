from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from Views import MainWindow
from Common.DebugPrint import myDebug, get_current_function_name
from Control import CameraController, ViewController
import sys
sys.path.append("../")

class MainController(QtCore.QObject):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(MainController, self).__init__(*arg)
        self.mMainLoopTimer = QtCore.QTimer(self)
        self.mViewController = ViewController.ViewController()
        self.initConnect()

    def start(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mViewController.start()
        self.mMainLoopTimer.start(50)

        self.mViewController.navigateTo("TestCameraWin")

    def initConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mMainLoopTimer.timeout.connect(self.mainLoop)

    def mainLoop(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        pass
    