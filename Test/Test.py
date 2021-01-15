import cv2
import numpy as np
import matplotlib.pyplot as plt
from Common import Common, XSetting
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject, QEvent, QCoreApplication, QSettings
import sys
sys.path.append('../')
import os

def testCamera():
    cap = cv2.VideoCapture(1)

    plt.figure("camera")
    while True:
        ret, frame = cap.read()
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

