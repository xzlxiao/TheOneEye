from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from Common.XSetting import XSetting
import cv2
import numpy as np
from Control import MainController
import math

'''
def qrDectbyZbar(frame):
    h1, w1 = frame.shape[0], frame.shape[1]

    texts = pyzbar.decode(frame)
    for text in texts:
        textdate = text.data.decode('utf-8')
        (x, y, w, h) = text.rect  # 获取二维码的外接矩形顶点坐标

        # 二维码中心坐标
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        cv2.circle(frame, (cx, cy), 2, (0, 255, 0), 8)  # 做出中心坐标
        # 画出画面中心与二维码中心的连接线
        cv2.line(frame, (cx, cy), (int(w1 / 2), int(h1 / 2)), (255, 0, 0), 10)
        # 二维码最小矩形
        try:
            cv2.line(frame, text.polygon[0], text.polygon[1], (255, 0, 0), 2)
            cv2.line(frame, text.polygon[1], text.polygon[2], (255, 0, 0), 2)
            cv2.line(frame, text.polygon[2], text.polygon[3], (255, 0, 0), 2)
            cv2.line(frame, text.polygon[3], text.polygon[0], (255, 0, 0), 2)
        except IndexError:
            pass
'''

# mindvision camera, tested in 1920x1200
newcameramtx = np.array(
 [[5.51867334e+03, 0.00000000e+00, 7.76432261e+02],
 [0.00000000e+00, 4.13022119e+03, 1.12034974e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array(
 [[-8.24964967e-02, -5.47742336e-01,  1.11060070e-02,
   -5.86555873e-03, 6.30614313e+00]])
mtx = np.array(
 [[1.87371833e+03, 0.00000000e+00, 9.66051669e+02],
 [0.00000000e+00, 1.90419363e+03, 5.66067640e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])


def qrDextbyArUco(frame, transM, mapw, maph, env_width, env_height):
    
    w = frame.shape[1]
    h = frame.shape[0]
    frame = cv2.warpPerspective(frame, transM, (w, h))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    angular = []
    centers = []

    if ids is not None:
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        (rvec - tvec).any()
        for i in range(rvec.shape[0]):
            
            cv2.aruco.drawAxis(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03)
            cv2.aruco.drawDetectedMarkers(frame, corners)

            # https://blog.csdn.net/dgut_guangdian/article/details/108093643
            R = np.zeros((3, 3), dtype=np.float64)
            cv2.Rodrigues(rvec[i, :, :], R)
            sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
            singular = sy < 1e-6
            if not singular:  # 偏航，俯仰，滚动
                # x = math.atan2(R[2, 1], R[2, 2])
                # y = math.atan2(-R[2, 0], sy)
                z = math.atan2(R[1, 0], R[0, 0])
            else:
                # x = math.atan2(-R[1, 2], R[1, 1])
                # y = math.atan2(-R[2, 0], sy)
                z = 0
            rz = -z
            angular.append([0, 0, rz])

        # print(angular)

        cornerarr = [i[0] for i in corners]
        centers = [np.sum(cornerarr[i], axis=0) / 4 for i in range(len(ids))]
        centers = [[(center[0] / mapw - 0.5) * env_width, (0.5-(center[1] / maph))*env_height, 0] for center in centers]
    return frame, ids, centers, angular


def initMap(frame, ratio):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if ids is None:
        return 0
    idarr = [i[0] for i in ids]
    cornerarr = [i[0] for i in corners]  # point（width(x), height(y)）
    vararr = [False for i in [0, 1, 2, 3] if i not in idarr]
    if vararr:
        return 0
    else:
        idindex = [idarr.index(i) for i in range(4)]
        cornerssquar = [cornerarr[i] for i in idindex]
        w = frame.shape[1]
        h = frame.shape[0]
        centers = [np.sum(cornerssquar[i], axis=0)/4 for i in range(4)]
        piccenter = (centers[0] + centers[1] + centers[2] + centers[3])/4
        mapbftrans = [0, 0, 0, 0]
        i = 0
        for center in centers:
            if center[0] < piccenter[0]:
                if center[1] < piccenter[1]:  # left top
                    for j in range(4):
                        if cornerssquar[i][j][0] < center[0] and cornerssquar[i][j][1] < center[1]:
                            mapbftrans[0] = cornerssquar[i][j]
                else:  # left button
                    for j in range(4):
                        if cornerssquar[i][j][0] < center[0] and cornerssquar[i][j][1] > center[1]:
                            mapbftrans[3] = cornerssquar[i][j]
            else:
                if center[1] < piccenter[1]:  # right top
                    for j in range(4):
                        if cornerssquar[i][j][0] >= center[0] and cornerssquar[i][j][1] < center[1]:
                            mapbftrans[1] = cornerssquar[i][j]
                else:  # right button
                    for j in range(4):
                        if cornerssquar[i][j][0] >= center[0] and cornerssquar[i][j][1] >= center[1]:
                            mapbftrans[2] = cornerssquar[i][j]
            i = i + 1

        mapaftrans = np.array([[0, 0], [w, 0], [w, int(w * ratio)], [0, int(w * ratio)]], dtype='float32')
        mapbftrans = np.array(mapbftrans, dtype='float32')
        transM = cv2.getPerspectiveTransform(mapbftrans, mapaftrans)

        print('init completed\n')
        # print('before={}\n'.format(mapbftrans))
        # print('after={}\n'.format(mapaftrans))
        # print('trans={}\n'.format(transM))
        return mapbftrans, mapaftrans, transM

env_width = float(XSetting.getValue('Epuck/ENVSIZE_WIDTH'))
env_height = float(XSetting.getValue('Epuck/ENVSIZE_HEIGHT'))

class ImageQR(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'二维码定位'
        self.mapInited = 0
        self.zbardetect = 0
        self.arucodetect = 1
        self.mapheight = 1200  # MindVision的相机的分辨率就是1920x1200，不是1920x1080
        self.mapwidth = 1920
        self.mapBfTrans = []
        self.mapAfTrans = []
        self.transM = None
        self.carIds = []
        self.posiCar = []
        self.poseCar = []

    def process(self, image: np.ndarray) -> np.ndarray:
        ret = super().process(image)
        # print(self.channels(image))
        if self.channels(image) == 1:
            pass
        elif self.channels(image) == 3:
            pass
        elif self.channels(image) == 4:
            image_tmp = image[:, :, 0:3]
            '''
            再此处添加算法，例如：
            image_tmp = 255 - image_tmp
            '''
            image_tmp = image_tmp.astype(np.uint8)
            if not self.mapInited:
                ret = initMap(image_tmp, ratio=(self.mapheight/self.mapwidth))
                if ret:
                    self.mapBfTrans = ret[0]
                    self.mapAfTrans = ret[1]
                    self.transM = ret[2]
                    self.mapInited = 1
            else:
                if self.arucodetect:
                    # 单个二维码测试耗时< 10 ms
                    image_tmp, self.carIds, self.posiCar, self.poseCar = qrDextbyArUco(image_tmp, self.transM, self.mapwidth, self.mapheight, env_width, env_height)
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image

            controller = MainController.getController()  # upload data to up-layer(shang ceng)
            if self.carIds is not None:
                for i in range(len(self.carIds)):
                    controller.mCameraData.setData('GlobalLocation', self.carIds[i][0],
                                                np.concatenate((self.posiCar[i], self.poseCar[i])))
        else:
            raise Exception('图像类型不支持')
        return ret
