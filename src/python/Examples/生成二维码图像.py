import cv2
import numpy as np
# 生成aruco标记
# 加载预定义的字典
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)

# 生成标记
markerImage = np.zeros((200, 200), dtype=np.uint8)
for i in range(50):
    markerImage = cv2.aruco.drawMarker(dictionary, i, 200, markerImage, 1)
    cv2.imwrite("/Volumes/disk3/test/mark/marker_4X4_%d.png" % i, markerImage)