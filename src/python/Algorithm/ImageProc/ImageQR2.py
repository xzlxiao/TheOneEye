from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np
from Control import MainController
import math



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


def qrDextbyArUco2(frame):
    w = frame.shape[1]
    h = frame.shape[0]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
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

            # # https://blog.csdn.net/dgut_guangdian/article/details/108093643
            # R = np.zeros((3, 3), dtype=np.float64)
            # cv2.Rodrigues(rvec[i, :, :], R)
            # sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
            # singular = sy < 1e-6
            # if not singular:  # 偏航，俯仰，滚动
            #     # x = math.atan2(R[2, 1], R[2, 2])
            #     # y = math.atan2(-R[2, 0], sy)
            #     z = math.atan2(R[1, 0], R[0, 0])
            # else:
            #     # x = math.atan2(-R[1, 2], R[1, 1])
            #     # y = math.atan2(-R[2, 0], sy)
            #     z = 0
            # # 偏航，俯仰，滚动换成角度
            # # rx = x * 180.0 / 3.141592653589793
            # # ry = y * 180.0 / 3.141592653589793
            # rz = z * 180.0 / 3.141592653589793
            # # distance = ((tvec[i][0][2] + 0.02) * 0.0254) * 100  # 单位是米
            # angular.append([0, 0, rz])

        cornerarr = [i[0] for i in corners]
        centers = [np.sum(cornerarr[i], axis=0) / 4 for i in range(len(ids))]
    return frame



class ImageQR2(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'二维码定位2'
        self.arucodetect = 1


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


            if self.arucodetect:
                image_tmp = qrDextbyArUco2(image_tmp)

            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret
