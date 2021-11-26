from Algorithm.RobotPolicy import RobotPolicyBase
from Entity.RobotEpuck import RobotEpuck
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QComboBox, QDialog


class RobotPolicyTest(RobotPolicyBase.RobotPolicyBase):
    def __init__(self):
        super().__init__()
        self.Name = 'RobotPolicyTest'
        self.mRobot:RobotEpuck
        self.isFirstRun = True

    def inputSetTarget(self):
        from Control.MainController import getController
        controller = getController()
        controller.mViewController.mCurrentWin.mFrameViewArea.releaseKeyboard()
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
        result = QInputDialog.getText(controller.mViewController.mCurrentWin,'Get Target Position','Target examp: 0.940, 0.425, 0, 0, 0, -30')
        if self.mRobot:
            target = result[0].split(',')
            self.mRobot.setTarget([float(i.strip()) for i in target])
            # print(self.mRobot.mTarget)
        controller.mViewController.mCurrentWin.mFrameViewArea.grabKeyboard()

    def update(self):
        # print('test RobotPolicyTest')
        if self.isFirstRun:
            self.inputSetTarget()
            self.isFirstRun = False
        self.mRobot.feedbackControl()

