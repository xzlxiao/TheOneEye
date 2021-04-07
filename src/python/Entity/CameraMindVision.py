from Entity.CameraBase import CameraBase
try: 
    import Common.mvsdk as mvsdk
except:
    mvsdk = None
    print('Driver of MB_SUA202GC could not be inited.')
from PyQt5.QtCore import QTimer,QDateTime
import numpy as np
from PyQt5.QtGui import QImage

class CameraMindVision(CameraBase):
    def __init__(self, *args, camera_info):
        super().__init__(*args)
        self.mTimerReadFrame = QTimer(self)
        self.mTimerReadFrame.timeout.connect(self.readFrame)
        self.cap = None
        self.pFrameBuffer = None
        self.DevInfo = camera_info
        self.mRate = 20

    def openCamera(self):
        if not mvsdk:
            print('Fail to open camera. ')
            return 

        if not self.mCameraOpened:
            self.mCameraOpened = True

            # 打开相机
            hCamera = 0
            try:
                hCamera = mvsdk.CameraInit(self.DevInfo, -1, -1)
            except mvsdk.CameraException as e:
                print("CameraInit Failed({}): {}".format(e.error_code, e.message) )
                return False
                
            # 获取相机特性描述
            cap = mvsdk.CameraGetCapability(hCamera)

            # 判断是黑白相机还是彩色相机
            monoCamera = (cap.sIspCapacity.bMonoSensor != 0)

            # 相机让ISP展成R=G=B的24位灰度
            mvsdk.CameraSetIspOutFormat(hCamera, mvsdk.CAMERA_MEDIA_TYPE_BGR8)

            # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
            FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * 3

            # 分配RGB buffer，用来存放ISP输出的图像
            # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
            pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)

            # 相机模式切换成连续采集
            mvsdk.CameraSetTriggerMode(hCamera, 0)

            # 手动曝光，曝光时间30ms
            mvsdk.CameraSetAeState(hCamera, 0)
            # 曝光时间10ms
            mvsdk.CameraSetExposureTime(hCamera, 10 * 1000)
            # 曝光gain = 30
            mvsdk.CameraSetAnalogGain(hCamera, 30)
            # ISP color gain & saturation
            mvsdk.CameraSetGain(hCamera, 106, 100, 110)
            mvsdk.CameraSetSaturation(hCamera, 99)
            
            # 让SDK内部取图线程开始工作
            mvsdk.CameraPlay(hCamera)

            self.mCameraId = hCamera
            self.pFrameBuffer = pFrameBuffer
            self.cap = cap
            self.mTimerReadFrame.start(1000/self.mRate)
    
    def releaseCamera(self):
        if self.mCameraOpened:
            mvsdk.CameraUnInit(self.mCameraId)
            self.mCameraId = 0
            if self.pFrameBuffer:
                mvsdk.CameraAlignFree(self.pFrameBuffer)

            self.mTimerReadFrame.stop()

            self.mCameraOpened = False
            self.signalReleased.emit()


    def readFrame(self):
        # 从相机取一帧图片
        hCamera = self.mCameraId
        pFrameBuffer = self.pFrameBuffer
        try:
            pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
            mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
            mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)
            
            # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
            # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
            frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape(FrameHead.iHeight, FrameHead.iWidth, 3)
            self.mFrame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
            self.mViewCamera.mImage = self.mFrame
        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )
            return

    def setRate(self, rate):
        self.mRate = rate 
        self.mTimerReadFrame.stop()
        self.mTimerReadFrame.start(1000/self.mRate)

    