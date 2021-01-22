import time,sys
from PyQt5 import QtWidgets,QtMultimediaWidgets, QtGui
from  PyQt5.QtMultimedia import  QCamera,QCameraImageCapture,QCameraViewfinderSettings
import CameraWin
from PyQt5.QtWidgets import QPushButton
import cv2
import PyQt5
import numpy as np

def qimage2numpy(qimage: PyQt5.QtGui.QImage, dtype='array'):
    """Convert QImage to numpy.ndarray.  The dtype defaults to uint8
    for QImage.Format_Indexed8 or `bgra_dtype` (i.e. a record array)
    for 32bit color images.  You can pass a different dtype to use, or
    'array' to get a 3D uint8 array for color images."""
    result_shape = (qimage.height(), qimage.width())
    temp_shape = (qimage.height(),
                  qimage.bytesPerLine() * 8 / qimage.depth())
    if qimage.format() in (QtGui.QImage.Format_ARGB32_Premultiplied,
                           QtGui.QImage.Format_ARGB32,
                           QtGui.QImage.Format_RGB32):
        if dtype == 'rec':
            dtype = QtGui.bgra_dtype
        elif dtype == 'array':
            dtype = np.uint8
            result_shape += (4,)
            temp_shape += (4,)
    elif qimage.format() == QtGui.QImage.Format_Indexed8:
        dtype = np.uint8
    else:
        raise ValueError("qimage2numpy only supports 32bit and 8bit images")
        # FIXME: raise error if alignment does not match
    buf = qimage.bits().asstring(qimage.numBytes())
    result = np.frombuffer(buf, dtype).reshape(temp_shape)
    if result_shape != temp_shape:
        result = result[:, :result_shape[1]]
    if qimage.format() == QtGui.QImage.Format_RGB32 and dtype == np.uint8:
        result = result[..., :3]
    result = result[:,:,::-1]
    return result

def qimage2numpy2(qimg):
    ptr = qimg.constBits()
    ptr.setsize(qimg.byteCount())

    mat = np.array(ptr).reshape(qimg.height(), qimg.width(), 4)  # 注意这地方通道数一定要填4，否则出错
    return mat

class CameraMainWin(QtWidgets.QMainWindow,CameraWin.CameraWin):
    def __init__(self):
        super(CameraMainWin, self).__init__()
        self.setupUi(self)
        #定义相机实例对象并设置捕获模式
        self.camera = QCamera()
        self.camera.setCaptureMode(QCamera.CaptureViewfinder)
        self.cameraOpened = False# 设置相机打开状态为未打开
        #设置取景器分辨率
        viewFinderSettings =  QCameraViewfinderSettings ()
        viewFinderSettings.setResolution(800,600)
        self.camera.setViewfinderSettings(viewFinderSettings)
        #初始化取景器
        self.viewCamera = QtMultimediaWidgets.QCameraViewfinder(self)
        self.camera.setViewfinder(self.viewCamera)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camerLayout.addWidget(self.viewCamera)  #取景器放置到预留的布局中
        #设置图像捕获
        self.capture = QCameraImageCapture(self.camera)
        self.capture.setCaptureDestination(QCameraImageCapture.CaptureToBuffer) #CaptureToBuffer
        self.switchCamera: QPushButton
        self.switchCamera.clicked.connect(self.SwitchCamera)
        self.takePic.clicked.connect(self.TakePic)
        self.capture.error.connect(lambda i, e, s: self.alert(s))
        self.capture.imageAvailable.connect(self.saveImage)
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image %04d captured" % self.save_seq))

    #相机（摄像头）开关处理
    def SwitchCamera(self):
        if not self.cameraOpened:
            print('test1')
            self.camera.start()
            print('test2')
            self.cameraOpened = True
            self.switchCamera.setText("关闭摄像头")
        else:
            self.camera.stop()
            self.cameraOpened = False
            self.switchCamera.setText("打开摄像头")

    def TakePic(self):#拍照响应槽函数，照片保存到文件
        FName = fr"/Users/xiaozhenlong/Desktop/tmp/{time.strftime('%Y%m%d%H%M%S', time.localtime())}" #文件名初始化
        print(self.capture.capture(FName + '.jpg'))
        print(f"捕获图像保存到文件：{FName}.jpg")

    def saveImage(self, requestId, image):
        print('test3')
        image: PyQt5.QtMultimedia.QVideoFrame
        image = qimage2numpy2(image.image())
        print(image.shape)
        cv2.imwrite('/Users/xiaozhenlong/Desktop/tmp/test3.jpg', image)
        # cv2.namedWindow('test')
        # cv2.imshow('test', image)
        # cv2.waitKey()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    W = CameraMainWin()
    W.show()
    sys.exit(app.exec_())