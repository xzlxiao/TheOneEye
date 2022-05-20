from PyQt5.QtCore import pyqtSignal, QObject, QEvent
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpathes
from PyQt5.QtWidgets import QWidget

class RobotBase(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.mRobotType = "RobotBase"
        self.mId = -1
        self.mPos = np.array([0, 0, 0], dtype=np.float32)
        self.mOrientation = np.zeros((3, 3), dtype=np.float)
        self.mTarget = np.array(self.mPos, dtype=np.float32)
        self.mTargetOrientation = np.array(self.mOrientation, dtype=np.float)
        
        self.mColor = 'red'
        self.mShape = 'circle_line'
        self.mRadius = 7
        self.image = None
        self.setRadius(self.mRadius)
        self.setColor(self.mColor)
        self.mWindow = None
        self.mAlpha = 1.0
        self.mPopulation = None 
        self.mObstacle = None 
        self.mAx = None

    def setTarget(self, target):
        '''
            target: 1 x 6, x y z rx ry rz
        '''
        self.mTarget = np.array(target[0:3], dtype=np.float32)
        

    def setColor(self, color=(255, 0, 0)):
        self.mColor = color
        self.setShape(self.mShape)
    
    def setRadius(self, radius=5):
        self.mRadius = radius
        self.setShape(self.mShape)

    @property
    def pos(self):
        return np.ndarray.tolist(self.mPos)

    @pos.setter
    def pos(self, value):
        self.mPos = np.array(value, dtype=np.float32)

    def getPos2d(self):
        return self.mPos[0:2]

    def setShape(self, shape='circle'):
        self.mShape = shape
        if shape=='circle':     # 实心圆
            self.image = mpathes.Circle(self.mPos[0:2], radius=self.mRadius, color=self.mColor, fill=True)
        elif shape=='circle_line':      # 圆圈
            self.image = mpathes.Circle(self.mPos[0:2], radius=self.mRadius, color=self.mColor,fill=False)
        elif shape=='square':     # 实心方块
            self.image = mpathes.Rectangle(self.mPos[0:2], self.mRadius*2, self.mRadius*2, color=self.mColor, fill=True)
        elif shape=='square_line':    # 空心方块
            self.image = mpathes.Rectangle(self.mPos[0:2], self.mRadius*2, self.mRadius*2, color=self.mColor, fill=False)
        else:
            raise RuntimeError('没有该预定义形状')

    @property
    def target(self):
        return np.ndarray.tolist(self.mTarget)

    @target.setter
    def target(self, value):
        self.mTarget = np.array(value, dtype=np.float32)

    def sense(self):
        """
        观察周围，感知区域为圆形
        :return: 障碍物位置 机器人位置
        """
        pass 

    def distance(self, pt1, pt2):
        """
        计算两点间的距离
        :param pt1: list or np.array
        :param pt2: list or np.array
        :return:
        """
        pt1 = np.array(pt1[0:3], dtype=np.float32)
        pt2 = np.array(pt2[0:3], dtype=np.float32)
        return np.linalg.norm(pt2 - pt1, ord=2)

    def move(self):
        """
        向目标移动一步
        :return:
        """
        pass

    def update(self):
        """

        :return:
        """
        self.move()

    def setAx(self, ax):
        self.mAx = ax

    def drawOnFigure(self, ax, label=''):
        ax.add_patch(self.image)
        art3d.pathpatch_2d_to_3d(self.image, z=self.mPos[2], zdir='z')