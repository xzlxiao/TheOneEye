from Entity.RobotEpuck import RobotEpuck
from Entity.CameraEPuck import CameraEPuck
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
import numpy as np
import math
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name

class RobotTwinsEpuck(RobotEpuck):
    def __init__(self, parent, population, pos=..., orientation=...) -> None:
        super().__init__(parent, population, pos, orientation)
        self.mRobotType = "RobotTwinsEpuck"