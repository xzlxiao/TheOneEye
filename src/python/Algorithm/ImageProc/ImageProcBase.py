import cv2 
import numpy as np
import copy

class ImageProcBase:
    def __init__(self) -> None:
        self.Name = 'ImageProcBase'
        self.mLastImage = None

    def channels(self, image):
        if image.ndim == 2:		#2维度表示长宽
            n_channels = 1 		#单通道(grayscale)
        elif image.ndim == 3:		
            n_channels = image.shape[-1]	#第三维度表示通道，应为3
        else:					#异常维度，不是图片了
            return -1
        return n_channels

    def process(self, image: np.ndarray) -> np.ndarray:
        return image

    def getConfig(self):
        return None

    def setConfig(self):
        pass

    def getName(self):
        return self.Name