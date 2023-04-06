from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np
from Control import MainController
import math
from Common.Common import Common



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

def findDirectionPos(pos_list):
    '''
    找出上下左右的极点
    '''
    ret_left = (0, 0)
    ret_right = (0, 0)
    ret_up = (0, 0)
    ret_down = (0, 0)
    for pos in pos_list:
        if pos[0] < ret_left[0]:
            ret_left = pos 
        if pos[0] > ret_right[0]:
            ret_right = pos 
        if pos[1] < ret_down[1]:
            ret_down = pos 
        if pos[1] > ret_up[1]:
            ret_up = pos 
    return ret_up, ret_down, ret_left, ret_right

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
    marker_dictionary = cv2.aruco.getPredefinedDictionary(7)
    if ids is not None:
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        # for i in range(rvec.shape[0]):
        #     cv2.aruco.drawAxis(frame, mtx, dist, rvec[0, :, :], tvec[0, :, :], 0.06)
        # cv2.aruco.drawDetectedMarkers(frame, corners)

        cornerarr = [i[0] for i in corners]
        # print(cornerarr[0])
        # cornerarr 是二维码上四个角点的点集，当x轴朝上时，角点顺序是 左下 左上 右上 右下
        centers = [np.sum(cornerarr[i], axis=0) / 4 for i in range(len(ids))]
        # pos_front = 
        direction_pos = []
        for i, id in enumerate(ids):
            if id == 999:
                cv2.aruco.drawAxis(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.06)
                cv2.aruco.drawDetectedMarkers(frame, [corners[i]])
            else:
                center = centers[i]
                pt1_ind = 1
                pt2_ind = 2
                x = (cornerarr[i][pt1_ind][0]+cornerarr[i][pt2_ind][0])/2 - center[0]
                y = (cornerarr[i][pt1_ind][1]+cornerarr[i][pt2_ind][1])/2 - center[1]
                pos_front = np.array((x, y))
                direction_pos.append((x, y))

                pt1_ind = 3
                pt2_ind = 0
                x = (cornerarr[i][pt1_ind][0]+cornerarr[i][pt2_ind][0])/2 - center[0]
                y = (cornerarr[i][pt1_ind][1]+cornerarr[i][pt2_ind][1])/2 - center[1]
                direction_pos.append((x, y))

                pt1_ind = 0
                pt2_ind = 1
                x = (cornerarr[i][pt1_ind][0]+cornerarr[i][pt2_ind][0])/2 - center[0]
                y = (cornerarr[i][pt1_ind][1]+cornerarr[i][pt2_ind][1])/2 - center[1]
                direction_pos.append((x, y))

                pt1_ind = 2
                pt2_ind = 3
                x = (cornerarr[i][pt1_ind][0]+cornerarr[i][pt2_ind][0])/2 - center[0]
                y = (cornerarr[i][pt1_ind][1]+cornerarr[i][pt2_ind][1])/2 - center[1]
                direction_pos.append((x, y))

                pos_up, pos_down, pos_left, pos_right = findDirectionPos(direction_pos)
                axes_len = (int(Common.distance(pos_left, pos_right)), int(Common.distance(pos_up, pos_down)))
                angle = Common.angle_with_x_axis(pos_right)*180/math.pi
                # center = np.array(center)
                center_int = (int(center[0]), int(center[1]))
                frame = cv2.ellipse(frame, center_int, axes_len, angle, 0, 360, (255,100,100,1), 5)
                center = np.array(center)
                pt2 = pos_front * 4 + center
                pt2 = (int(pt2[0]), int(pt2[1]))
                frame = cv2.arrowedLine(frame, center_int, pt2, (0, 255, 0, 1), 8, cv2.LINE_4)
                frame = cv2.putText(frame, 'ID: %d'%id, center_int, cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255, 1), 5)
    return frame



class ImageQR_RobotMarker(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'机器人marker绘制测试'
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
