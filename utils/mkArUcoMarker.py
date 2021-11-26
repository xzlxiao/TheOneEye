import cv2
import numpy as np
# 生成aruco标记
# 加载预定义的字典
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)
id=68

# 生成标记
markerImage = np.zeros((2000, 2000), dtype=np.uint8)
markerImage = cv2.aruco.drawMarker(dictionary, id, 2000, markerImage, 1)
print(cv2.imwrite("../../../data/images/marker68.png", markerImage))
