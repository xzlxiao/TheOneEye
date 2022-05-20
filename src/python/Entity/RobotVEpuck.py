from typing import overload
from Entity.RobotEpuck import RobotEpuck
from Entity.CameraEPuck import CameraEPuck
from PyQt5.QtCore import pyqtSignal, QObject, QEvent
import numpy as np
import math
from Common.XSetting import XSetting
from Common.DebugPrint import myDebug, get_current_function_name
import socket
import cv2
import threading
import struct
import time

class VEpuckConnector:
    def __init__(self, D_addr_port=["", 8881]):
        self.resolution = [1600, 1200]
        self.addr_port = D_addr_port
        self.src = 888 + 15  # 双方确定传输帧数，（888）为校验值
        self.interval = 0  # 图片播放时间间隔
        self.img_fps = 15  # 每秒传输多少帧数
        

    def Set_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def Socket_Connect(self):
        self.Set_socket()
        self.client.connect(self.addr_port)
        print("IP is %s:%d" % (self.addr_port[0], self.addr_port[1]))

    def RT_Image(self, robot):
        # 按照格式打包发送帧数和分辨率
        # 
        self.name = self.addr_port[0] + " Camera"
        self.client.send(struct.pack("ihh", self.src, self.resolution[0], self.resolution[1]))
        count = 0
        while (not robot.isFinished):
            print(count)
            count += 1
            info = struct.unpack("ihh", self.client.recv(8))
            buf_size = info[0]  # 获取读的图片总长度
            # print("图片总长度：%i" % buf_size)
            if buf_size:
                try:
                    self.buf = b""  # 代表bytes类型
                    temp_buf = self.buf
                    while (buf_size):  # 读取每一张图片的长度
                        time.sleep(1.0/self.img_fps)
                        temp_buf = self.client.recv(buf_size)
                        buf_size -= len(temp_buf)
                        self.buf += temp_buf  # 获取图片
                        data = np.fromstring(self.buf, dtype='uint8')  # 按uint8转换为图像矩阵
                        self.image = cv2.imdecode(data, 1)  # 图像解码
                        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
                        robot.setImage(self.image.copy())
                  
                        # cv2.waitKey(1)
                        # cv2.imwrite("/Users/xzlxiao/tmp/" + mytime + ".jpg", self.image)
                except:
                    pass

    def Get_Data(self, robot):
        showThread = threading.Thread(target=self.RT_Image, args=(robot,))
        showThread.start()

class RobotVEpuck(RobotEpuck):
    def __init__(self, parent, population, pos=np.array((0, 0, 0), dtype=np.float), orientation = np.zeros((3,3), dtype=np.float)) -> None:
        super().__init__(parent, population, pos, orientation)
        self.mRobotType = "RobotTwinsEpuck"
        self.client_addr = "127.0.0.1"
        self.connector = None
        self.isFinished = False

    def initCommand(self):
        myDebug(self.__class__.__name__, get_current_function_name())
        pass

    def __del__(self):
        print("test_del")
        self.isFinished = True

    def setSpeed(self, motor_L, motor_R):
        myDebug(self.__class__.__name__, get_current_function_name())
        print("motor_L: %f, motor_R: %f"%(motor_L, motor_R))
        pass

    def update(self):
        pass

    def connect(self, dir):
        self.client_addr, self.client_sock = dir.split(":")
        self.connector = VEpuckConnector(D_addr_port=(self.client_addr, int(self.client_sock)))
        self.connector.addr_port = tuple(self.connector.addr_port)
        self.connector.Socket_Connect()
        self.connector.Get_Data(self)

    def setImage(self, image):
        self.mCamera.updateFrame(image)