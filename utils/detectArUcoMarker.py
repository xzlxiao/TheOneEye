# python3 /Volumes/disk3/Code/research/TheOneEye/utils/detectArUcoMarker.py --image /Volumes/disk3/实验数据/mark/marker_4x4_1000_917.png --type DICT_4X4_1000
import argparse
import cv2
import sys
import numpy as np
import math
dist = np.array(
 [[-8.24964967e-02, -5.47742336e-01,  1.11060070e-02,
   -5.86555873e-03, 6.30614313e+00]])
mtx = np.array(
 [[1.87371833e+03, 0.00000000e+00, 9.66051669e+02],
 [0.00000000e+00, 1.90419363e+03, 5.66067640e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
 
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image containing the ArUCo tag")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Tpe of ArUCo tag to detect")
args = vars(ap.parse_args())

ARUCO_DICT = {"DICT_4X4_50": cv2.aruco.DICT_4X4_50, "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
              "DICT_4X4_250": cv2.aruco.DICT_4X4_250, "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
              "DICT_5X5_50": cv2.aruco.DICT_5X5_50, "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
              "DICT_5X5_250": cv2.aruco.DICT_5X5_250, "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
              "DICT_6X6_50": cv2.aruco.DICT_6X6_50, "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
              "DICT_6X6_250": cv2.aruco.DICT_6X6_250, "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
              "DICT_7X7_50": cv2.aruco.DICT_7X7_50, "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
              "DICT_7X7_250": cv2.aruco.DICT_7X7_250, "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
              "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
              "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
              "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
              "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
              "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11}

print("[INFO] Loading image...")
image = cv2.imread(args["image"])

if ARUCO_DICT.get(args["type"], None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported!".format(args["type"]))
    sys.exit(0)

print("[INFO] Detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
print((corners, ids, rejected))
if len(corners) > 0:
    ids = ids.flatten()
    # 循环检测到的 ArUCo 标记
    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
    for i in range(rvec.shape[0]):
        cv2.aruco.drawAxis(image, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03)
        cv2.aruco.drawDetectedMarkers(image, corners)
        R = np.zeros((3, 3), dtype=np.float64)
        cv2.Rodrigues(rvec[i, :, :], R)
        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6
        if not singular:  # 偏航，俯仰，滚动
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0
        # 偏航，俯仰，滚动换成角度
        rx = x * 180.0 / math.pi
        ry = y * 180.0 / math.pi
        rz = z * 180.0 / math.pi
        print('rx: {}, ry: {}, rz: {}'.format(rx, ry, rz))
    
    for (markerCorner, markerID) in zip(corners, ids):
        # 提取始终按​​以下顺序返回的标记：
        # TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM-LEFT
        
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # 将每个 (x, y) 坐标对转换为整数
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        # 绘制ArUCo检测的边界框
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
        # 计算并绘制 ArUCo 标记的中心 (x, y) 坐标
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
        # 在图像上绘制 ArUco 标记 ID
        cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] ArUco marker ID: {}".format(markerID))
        # 显示输出图像
        cv2.imshow("Image", image)
        cv2.waitKey(0)
