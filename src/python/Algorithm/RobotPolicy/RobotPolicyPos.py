from Algorithm.RobotPolicy import RobotPolicyBase
from Entity.RobotEpuck import RobotEpuck
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox, QDialog


class RobotPolicyPos(RobotPolicyBase.RobotPolicyBase):
    def __init__(self):
        super().__init__()
        self.Name = '直接指定坐标'
        self.mRobot:RobotEpuck
        self.isFirstRun = True

        self.targetsForOneRobot = []

    def inputTargets(self):
        from Control.MainController import getController
        controller = getController()
        controller.mViewController.getCurrentWin().mFrameViewArea.releaseKeyboard()
        # dialog = QInputDialog(controller.mViewController.mCurrentWin)
        # dialog.setModal(True)
        # dialog.setStyleSheet("""
        # background-color: rgba(0, 0, 0, 200);
        # border:1px solid rgba(0, 200, 200, 150);
        # """)
        # dialog.setFixedSize(350,250)
        # dialog.setWindowTitle('Get Target Position')
        # dialog.setInputMode(QInputDialog.TextInput)
        # dialog.textValueSelected.connect(lambda text_: print(text_))
        # dialog.show()


        # results = QInputDialog.getText(controller.mViewController.mCurrentWin,'Get Target Position','Target examp: 0.940, 0.425, 0, 0, 0, -30')
        # # if self.mRobot:
        # #     target = result[0].split(',')
        #     # self.mRobot.setTarget([float(i.strip()) for i in target])
        #     # print(self.mRobot.mTarget)
        # print('results: ', results)
        # targets = results[0].split(';')
        # for result in targets:
        #     target = result.split(',')
        #     self.targetsForOneRobot.append([float(i.strip()) for i in target])
        # self.mRobot.setTarget(self.targetsForOneRobot[0])  # set the first target
        # self.targetsForOneRobot.pop(0)
        # controller.mViewController.mCurrentWin.mFrameViewArea.grabKeyboard()
        # print(self.targetsForOneRobot)
        # self.targetsForOneRobot = [[-0.1664, 0.015,0,0,0,29], [0,0,0,0,0,0], [0.15, -0.087, 0, 0,0, -30.6], [0.3223, -0.27, 0,0,0,0]]
        self.targetsForOneRobot = [[0.0, 0.0, 0,0,0,60]]
        self.mRobot.setTarget(self.targetsForOneRobot[0])
        self.targetsForOneRobot.pop(0)

    def setRobotTarget(self):  # only set target,rather than control
        if self.mRobot.toNextTarget and len(self.targetsForOneRobot) > 0:
            self.mRobot.setTarget(self.targetsForOneRobot[0])  # set the next target
            self.targetsForOneRobot.pop(0)
            self.mRobot.toNextTarget = False

    def update(self):
        # print('test RobotPolicyTest')
        if self.isFirstRun:
            self.inputTargets()
            self.isFirstRun = False
        self.setRobotTarget()  #
        self.mRobot.feedbackControl()

