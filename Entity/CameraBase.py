from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")
from PyQt5.QtCore import pyqtSignal, QObject, QEvent


class CameraBase(QObject):
    def __init__(self, *args):
        super(CameraBase, self).__init__(*args)
        self.mCameraId = -1

    def openCamera(self):
        pass

    def releaseCamera(self):
        pass

    def setCameraID(self, id):
        self.mCameraId = id
