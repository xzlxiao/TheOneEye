# -*- coding: utf-8 -*-
import socket
import threading
import struct
import numpy as np

import sys
import time
import cv2

class CameraControl(object):
    def __init__(self, CameraNum=0):
        self.camera = self.createCamera(CameraNum)
        self.isSuccess, self.image = self.camera.read()
        self.sizeX = 640
        self.sizeY = 480
        self.writer = None

    def createCamera(self, CameraNum):
        return cv2.VideoCapture(CameraNum)

    def createWriter(self, dir="/Users/xzlxiao/result"):
        self.writer = cv2.VideoWriter(dir+"/"+get_time_stamp()+".mp4", cv2.VideoWriter_fourcc('m','p','4','v'), 20, (self.sizeX, self.sizeY))

    def writerCapture(self):
        self.writer.write(self.image)

    def writePicture(self, dir="/Users/xzlxiao/result"):
        self.capture()
        cv2.imwrite(dir+"/"+get_time_stamp()+".jpg", self.image)

    def capture(self):
        self.isSuccess, self.image = self.camera.read()

    def flip(self):
        self.image = cv2.flip(self.image, 1)

    def release(self):
        self.camera.release()

    def releaseWriter(self):
        self.writer.release()

    def setWindowSize(self, size):
        self.camera.set(3, size[0])
        self.camera.set(4, size[1])
        self.sizeX = size[0]
        self.sizeY = size[1]

    def isOpened(self):
        return self.camera.isOpened()


def get_time_stamp():
    """
    返回毫秒级时间戳
    ****年**月**日**小时**分**秒***毫秒
    :return:
    """
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s%03d" % (data_head, data_secs)
    return time_stamp




class Camera_Accept_Object:
    def __init__(self, S_addr_port = ("", 8881)):
        self.img_fps = 15       # 每秒传输多少帧数
        self.addr_port = S_addr_port
        self.Set_Socket(self.addr_port)
        self.resolution = (640, 480)
        self.img = None

    def Set_Socket(self, S_addr_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 端口可复用
        self.server.bind(S_addr_port)
        self.server.listen(5)


def check_option(object, client):
    info = struct.unpack('ihh', client.recv(8))
    if info[0] > 888:
        object.img_fps = int(info[0])-888       # 获取帧数
        object.resolution = list(object.resolution)
        # 获取分辨率
        object.resolution[0] = info[1]
        object.resolution[1] = info[2]
        object.resolution = tuple(object.resolution)
        return 1
    else:
        return 0

def RT_Image(object, client, D_addr, camera):
    if check_option(object, client) == 0:
        return
    img_param = [int(cv2.IMWRITE_JPEG_QUALITY), object.img_fps]
    camera.setWindowSize(object.resolution)
    count = 0
    while(1):
        count += 1
        print("图片发送: %i"%count)
        time.sleep(0.1)
        camera.capture()
        if camera.isSuccess:
            object.img = camera.image
            _, img_encode = cv2.imencode('.jpg', object.img, img_param)
            img_code = np.array(img_encode)
            object.img_data = img_code.tostring()
            try:
                # 按照相应格式进行打包发送图片
                client.send(struct.pack("ihh", len(object.img_data), object.resolution[0], object.resolution[1])+object.img_data)
            except:
                # camera.release()
                return

if __name__ == '__main__':
    object = Camera_Accept_Object()
    camera = CameraControl(0)
    print("开始发送数据")
    while(1):
        client, D_addr = object.server.accept()
        clientThread = threading.Thread(target=RT_Image, args=(object, client, D_addr, camera,))
        clientThread.start()

