import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import pyqtSignal, QObject, QEvent
# from PyQt5.QtCore import pyqtSignal, QObject, QEvent, QCoreApplication, QSettings
import sys
sys.path.append('../')
sys.path.append('./')
from Entity.CameraMindVision import CameraMindVision
from Common import Common, XSetting
from Entity.RobotEpuck import RobotEpuck
import time 
try: 
    import Common.mvsdk as mvsdk
except:
    mvsdk = None

def testCamera():
    cap = cv2.VideoCapture(0)

    plt.figure("camera")
    while True:
        ret, frame = cap.read()
        print(ret, frame)
        plt.imshow(frame)
        plt.show()


def test_MV_SUA_camera():
    app = QApplication(sys.argv)
    # 枚举相机
    if mvsdk:
        DevList = Common.mvsdk.CameraEnumerateDevice()
        nDev = len(DevList)
        if nDev < 1:
            print("No camera was found!")
            return

        for i, DevInfo in enumerate(DevList):
            print("{}: {} {}".format(i, DevInfo.GetFriendlyName(), DevInfo.GetPortType()))

        i = 0 if nDev == 1 else int(input("Select camera: "))
        cam = CameraMindVision(camera_info=DevList[i])
        cam.openCamera()
        cam.readFrame()
        cam.setRate(30)
        print(cam.mFrame)
        print('test')
    sys.exit(app.exec_())

def test_robot():
    app = QApplication(sys.argv)
    robot = RobotEpuck(None, None, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    try:
        robot.connect('192.168.3.5')
        if robot.isConnected:
            for i in range(3):
                # if i%1==0:
                #     print(i)
                if i < 3:
                    robot.mCommand[1] = 1
                    # robot.mCommand[8] = 1
                    # robot.mCommand[9] = 1
                    # robot.mCommand[10] = 1
                    # robot.mCommand[7] = 0x01
                    # robot.mCommand[17] = 100
                    # robot.mCommand[17] = 100
                    # robot.mCommand[17] = 100
                    # robot.mCommand[18] = 255
                    robot.setSpeed(0, 0)
                    robot.update()
                    time.sleep(1)
                # elif i < 20:
                #     robot.setSpeed(100, -100)
                #     robot.update()
                #     time.sleep(1)
                # robot.mCommand[4] = 0
                # robot.mCommand[6] = 0
                # robot.mCommand[3] = 0
                # robot.mCommand[5] = 0
                # robot.update()
                print(robot.mCommand[4], ' ', robot.mCommand[6], ' ', robot.mCommand[3], ' ', robot.mCommand[5])
                # time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        robot.setSpeed(0, 0)
        robot.disconnect()
    # sys.exit(app.exec_())
    



def testSettings():
    XSetting.XSetting.print()
    # print(XSetting.XSetting.getValue('Test/Name'))
    assert XSetting.XSetting.getValue('Test/Name') == 'Configuration'
    XSetting.XSetting.setValue("Test/Name2", "123")
    assert int(XSetting.XSetting.getValue("Test/Name2")) == int(123)
    XSetting.XSetting.removeValue("Test/Name2")
    assert XSetting.XSetting.getValue("Test/Name2") == "Fail"


def UnitTest():
    testSettings()

# if __name__=="__main__":
#     test_MV_SUA_camera()