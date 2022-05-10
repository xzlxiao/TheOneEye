from logging import BufferingFormatter
from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QDialog
from PyQt5.QtGui import QImage
import cv2 
import numpy as np
from Common.Common import Common
import cv2
from PIL import Image
import copy
import threading
import time
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from skvideo.io import FFmpegWriter 

lock = threading.Lock()
# Image2VideoInstance = {}
# processing_images_list_1 = []
# instances = {}
# isThreadStop = {}
# out = {}
# breakCount = {}
class Image2Video(ImageProcBase):
    
    _count = 0
    def __init__(self) -> None:
        super().__init__()
        self.id = Image2Video._count
        Image2Video._count += 1
        # instances[self.id] = self
        # breakCount[self.id] = 0
        self.count = 0
        # isThreadStop[self.id] = False
        self.Name = r'Video Save'
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.fps = 10  # 帧数
        self.width = 640
        self.height = 320
        self.save_seconds = 60      # 保存视频的时长
        self.out = None 
        self.processing_images_list = []
        self.processing_time_list = []
        try:
            Common.mkdir(self.mImageSaveDir)
        except:
            print('cannot create dir' + self.mImageSaveDir)


    def setImageSaveDir(self, dir):
        self.mImageSaveDir = dir
        Common.mkdir(self.mImageSaveDir)
        

    def process(self, image: np.ndarray) -> np.ndarray:
        ret = super().process(image)
        im = ret

        lock.acquire(True)
        self.processing_images_list.append(im)
        if len(self.processing_images_list)%(self.fps*self.save_seconds)==0:
            self.processing_time_list.append(Common.getDirTime())
        # self.processing_images.append(im)
        # self.t.processing_images_list.append(im)
            image_list = self.processing_images_list[0:self.fps*self.save_seconds]
            self.processing_images_list = self.processing_images_list[self.fps*self.save_seconds:]
            t = threading.Thread(target=self.thread_run, args=(image_list, self.processing_time_list.pop(0), self.mImageSaveDir, self.fps, (self.width, self.height)))
            t.start()
        lock.release()#释放
        
        
        # if not cv2.imwrite(save_name, ret):
        #     print('保存失败：' + save_name)
        # else:
        #     pass
        # save_image.show()
        return ret

    @staticmethod
    def thread_run(image_list:list, time_str:str, save_dir: str, fps:int, size:tuple):
        # print("test1-------------------------------")
        # print(id)
        # print(len(image_list))
        # fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        save_path = save_dir + '/video_' + time_str + '.mp4'
        # out = cv2.VideoWriter(save_path, fourcc, fps, size)
        writer = FFmpegWriter(save_path)
        # writer.open()
        for image in image_list:
            # print(image)
            # im = cv2.resize(image, size)
            writer.writeFrame(image)
        # out.release()
        writer.close()
        print('save video: ', save_path)

# class VideoProcessThread(QThread):
#     def __init__(self):
#         super(VideoProcessThread, self).__init__()
#         self.obj = None 
#         self.processing_images_list = []
#         self.id = -1

#     def receive_image(self, image):
#         self.processing_images_list.append(image)

#     def run(self):
#         # print("test1-------------------------------")
#         while not self.obj.isThreadStop:
#             # print("test2-------------------------------")
#             if len(self.processing_images_list) > 0:
#                 print("len of processing_images: {}".format(len(self.processing_images_list)))
#             lock.acquire(True)
#             if len(self.processing_images_list) > 0 and self.obj.out is not None:
#                 print("test3-------------------------------")
#                 im = self.processing_images_list.pop(0)
#                 im = cv2.resize(im, (self.obj.width, self.obj.height))
#                 # print("视频写入：", self.out.write(im))  # 写入帧
#                 # print(type(im))
#                 # print(im.shape)
#                 try:
#                     print("{}|".format(self.obj.count), im.shape)
#                     self.obj.out.write(im)
#                 except:
#                     print("fail to save video")
#             lock.release()#释放
#             time.sleep(0.02)
#         self.obj.out.release()