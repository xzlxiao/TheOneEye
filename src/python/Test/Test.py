import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import pyqtSignal, QObject, QEvent, QCoreApplication, QSettings
import sys
sys.path.append('../')
sys.path.append('./')
from Entity.CameraMindVision import CameraMindVision
from Common import Common, XSetting
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

if __name__=="__main__":
    test_MV_SUA_camera()