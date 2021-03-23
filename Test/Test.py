import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject, QEvent, QCoreApplication, QSettings
import sys
sys.path.append('../')
sys.path.append('./')
from Common import Common, XSetting


def testCamera():
    cap = cv2.VideoCapture(0)

    plt.figure("camera")
    while True:
        ret, frame = cap.read()
        print(ret, frame)
        plt.imshow(frame)
        plt.show()


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
    testCamera()