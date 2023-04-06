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
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    angular = []
    centers = []
    if ids is not None:
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        (rvec - tvec).any()
        print(rvec.shape)
        for i in range(rvec.shape[0]):
            cv2.aruco.drawAxis(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03)
            cv2.aruco.drawDetectedMarkers(frame, corners)

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
