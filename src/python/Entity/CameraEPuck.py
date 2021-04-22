from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")

from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings
import numpy as np
from Common.Common import Common
from PyQt5.QtGui import QImage
import time

class CameraEPuck(CameraBase.CameraBase):
    def __init__(self, *args, robot=None):
        super().__init__(*args)
        self.mRobot = robot

    def updateFrame(self, frame:np.ndarray):
        self.mFrame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

    def openCamera(self):
        self.mCameraOpened = True

    def releaseCamera(self):
        self.mCameraOpened = False