from Entity.RobotEpuck import RobotEpuck
from Entity.CameraEPuck import CameraEPuck
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
import numpy as np
import math
from Common.XSetting import XSetting

class RobotEpuckGRN(RobotEpuck):
    def __init__(self, parent: QObject, population, target_obstacle, pos) -> None:
        super().__init__(parent, population, target_obstacle, pos)
        self.__NurbsPoint = np.array([0.0, 0.0], dtype=np.float32)
        self.mP = np.array([0.0, 0.0])
        self.mC = float(XSetting.XSetting.getValue('GRN/C'))
        self.mR = float(XSetting.XSetting.getValue('GRN/R'))
        self.mB = float(XSetting.XSetting.getValue('GRN/B'))
        self.mA = float(XSetting.XSetting.getValue('GRN/A'))
        self.mM = float(XSetting.XSetting.getValue('GRN/M'))

    def setNurbsValue(self, value: float):
        self.nurbsValue = value

    def setNurbsPoint(self, point: np.ndarray):
        self.__NurbsPoint = point

    def update_P(self):
        self.mP += -self.mC * self.mP - self.mR * self.sigmoid_z() + self.mB * self.update_D()

    def update_target(self):
        self.mTarget += -self.mA * self.update_z() + self.mM * self.mP

    def sigmoid_z(self):
        z = self.update_z()
        # 防止数据太大导致溢出
        for index, val in enumerate(z):
            if val > 700:
                z[index] = 700
            elif val < -700:
                z[index] = -700
        #
        ret = (1 - np.power(math.e, -z))/(1 + np.power(math.e, -z))
        return ret

    def update_D(self):
        ret = np.array([0.0, 0.0])
        for robot in self.mPopulation:
            if self.distance(self.mPos, robot.mPos):
                ret += (self.mPos - robot.mPos)/self.distance(self.mPos, robot.mPos)
        return ret

    def update_z(self):
        return self.mPos - self.__NurbsPoint

    def update(self):
        """

        :return:
        """
        # print(self.mSpeed)
        self.update_P()
        self.update_target()
        self.move()