from Algorithm.RobotPolicy import RobotPolicyBase
from Entity.RobotEpuck import RobotEpuck
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox, QDialog


class RobotPolicyQR_pos(RobotPolicyBase.RobotPolicyBase):
    def __init__(self):
        super().__init__()
        self.Name = '以二维码999为目标'
        self.mRobot:RobotEpuck

    def updateTargets(self):
        from Control.MainController import getController
        controller = getController()
        controller.mViewController.getCurrentWin().mFrameViewArea.releaseKeyboard()
        target = controller.mCameraData.getData('GlobalLocation', 999)
        self.mRobot.setTarget(target)

    def update(self):
        self.updateTargets()  #
        self.mRobot.feedbackControl()

