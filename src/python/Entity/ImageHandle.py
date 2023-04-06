"""
       .==.        .==.
      //`^\\      //^`\\
     // ^ ^\(\__/)/^ ^^\\
    //^ ^^ ^/+  0\ ^^ ^ \\
   //^ ^^ ^/( >< )\^ ^ ^ \\
  // ^^ ^/\| v''v |/\^ ^ ^\\
 // ^^/\/ /  `~~`  \ \/\^ ^\\
 ----------------------------
BE CAREFULL! THERE IS A DRAGON.

Function：CameraHandle 摄像头图像处理

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-03-23 10:43:40 xzl
"""
import copy
import threading
from Common.DebugPrint import myDebug, get_current_function_name
import sys
sys.path.append("../")
sys.path.append("./")
from functools import partial
from Entity import CameraBase
from PyQt5 import  QtWidgets,QtMultimediaWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QTimer, QThread, QObject
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraViewfinderSettings
import numpy as np
from Common.Common import Common
from Views import XLabel
from Entity.CameraInterface import CameraInterface
import copy
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from Entity.HandleBase import HandleBase

lock = threading.Lock()

class ImageHandle(HandleBase):
    _count = 0
    def __init__(self, image_flow=None):
        super().__init__()
        self.id = ImageHandle._count
        ImageHandle._count += 1
        self.image_label.mBackImage.load("resource/images/EyeOfSauron.jpeg")
        self.image_label.hide()
        self.mProcessList = []     # 函数指针列表 func(image_src)->image_dst
        self.mImageFlow = image_flow
        self.Image_Processing = None
        self.isProcessing = False
        self.imageProcessThreadList = {}
        self.threadCount = 0
        self._imageSaveDir = ""

    def setImageSaveDir(self, dir: str):
        self._imageSaveDir = dir 
        for image_proc in self.mProcessList:
            image_proc.mImageSaveDir = self._imageSaveDir

    def image_process(self):
        # if self.mImageFlow:
        #     print(self.mImageFlow.mFrame)
        # print(self.Image_Processing)
        if self.mImageFlow:
            if self.mImageFlow.mFrame is not None:
                if len(self.mProcessList):
                    if not self.isProcessing:
                        self.isProcessing = True

                        if self.Image_Processing is not None:
                            self.image_label.mImage = Common.numpy2QImage(self.Image_Processing) 
                        else:
                            self.image_label.mImage = self.mImageFlow.mFrame.copy()

                        image = self.mImageFlow.mFrame
                        
                        image = Common.qImage2Numpy(image.convertToFormat(QImage.Format_ARGB32), 4)
                        t = threading.Thread(target=ImageHandle.image_process_thread, args=(image, self))
                        t.start()
                        # t = ImageProcessThread()
                        # self.imageProcessThreadList[self.threadCount] = t
                        # t.id = self.threadCount
                        # self.threadCount += 1
                        # t.obj = self 
                        # t.image = image 
                        # t.finished.connect(partial(self.threadFinished, t.id))
                        # t.start()
                        # t.quit()
                        # t.wait()
                        
                    else:
                        # img = self.mImageFlow.mFrame.copy()
                        pass
                else:
                    self.image_label.mImage = self.mImageFlow.mFrame.copy()
                self.image_label.update()
        elif self.image_label.mImage:
            self.image_label.mImage = None

    def threadFinished(self, id):
        self.imageProcessThreadList[id] = None 

    @staticmethod
    def image_process_thread(image, obj):
        try:
            # lock.acquire(True)
            for image_proc in obj.mProcessList:
                obj.Image_Processing = image_proc.process(image)
        finally:
            obj.isProcessing = False
            # lock.release()#释放
            # pass
    
    def setImageFlow(self, flow):
        self.mImageFlow = flow 

    def addImageProcess(self, im_proc: ImageProcBase, index=-1):
        im_proc.setImageSaveDir(self._imageSaveDir)
        if index == -1 or len(self.mProcessList)==0:
            self.mProcessList.append(im_proc)
        elif index < len(self.mProcessList) and index >= 0:
            self.mProcessList.insert(index, im_proc)
        else: 
            raise Exception('超出范围')

    def removeImageProcess(self, index):
        if index >= 0 and index < len(self.mProcessList):
            self.mProcessList.pop(index)
        else: 
            raise Exception('超出范围')

    def getImageProcNames(self):
        ret = []
        for i in self.mProcessList:
            ret.append(i.Name)

        return ret


class ImageProcessThread(QThread):
    def __init__(self):
        super(ImageProcessThread, self).__init__()
        self.obj = None 
        self.image = None
        self.id = -1
    def run(self):
        try:
            # lock.acquire(True)
            for image_proc in self.obj.mProcessList:
                self.obj.Image_Processing = image_proc.process(self.image)
        finally:
            if self.obj is not None:
                self.obj.isProcessing = False
            # lock.release()#释放
            # pass