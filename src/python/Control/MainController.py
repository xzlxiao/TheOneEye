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

Function：The controller of the app

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 09:38:15 xzl
"""
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from Views import MainWindow
from Common.DebugPrint import myDebug, get_current_function_name
from Control import CameraController, ViewController, CameraController, RobotController
from Entity.CameraData import CameraData
from Entity.ImageHandle import ImageHandle
import time
import sys
sys.path.append("../")

__controller = None

class MainController(QtCore.QObject):
    def __init__(self, *arg):
        myDebug(self.__class__.__name__, get_current_function_name())
        super(MainController, self).__init__(*arg)
        self.mMainLoopTimer = QtCore.QTimer(self)
        self.mViewController = ViewController.ViewController()
        self.mCameraController = CameraController.CameraController()
        self.mRobotController = RobotController.RobotController()
        self.mCameraData = CameraData()         # 公共变量资源
        self.mImageHandle = []
        self.initConnect()
        self.t1 = 0.0

    def start(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mViewController.start()
        self.mRobotController.start()
        self.mMainLoopTimer.start(1000/30)

        self.mViewController.navigateTo("ContentsNavWin")

    def initConnect(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        self.mMainLoopTimer.timeout.connect(self.mainLoop)

    def mainLoop(self):
        # myDebug(self.__class__.__name__, get_current_function_name())
        # t2 = time.time()
        # print('总时间：', t2 - self.t1)
        # self.t1 = t2
        # t1 = time.time()
        self.mCameraController.run()
        for handle in self.mImageHandle:
            # t1 = time.time()
            handle.image_process()
        # t2 = time.time()
        # print('计算时间：', t2-t1)

    
    def addImageHandle(self, image_handle: ImageHandle):
        self.mImageHandle.append(image_handle)

    def removeImageHandle(self, image_handle: ImageHandle):
        self.mImageHandle.remove(image_handle)

    def getInputFlowList(self):
        camera_list = self.mCameraController.getCameraList()
        video_list = []
        robot_list = []
        ret = []
        ret.extend(camera_list)
        ret.extend(video_list)
        ret.extend(robot_list)
        return ret

def getController()->MainController:
    return __controller