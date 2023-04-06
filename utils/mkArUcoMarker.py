import cv2
import numpy as np
# 生成aruco标记
# 加载预定义的字典
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
id=917

# 生成标记
markerImage = np.zeros((500, 500), dtype=np.uint8)
markerImage = cv2.aruco.drawMarker(dictionary, id, 500, markerImage, 1)
markerImage2 = np.zeros((600, 600), dtype=np.uint8)
markerImage2 += 255
markerImage2[50:550, 50:550] = markerImage
print(cv2.imwrite("/Volumes/disk3/实验数据/mark/marker_4x4_1000_917.png", markerImage))
