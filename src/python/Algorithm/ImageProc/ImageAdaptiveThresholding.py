from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np


class ImageAdaptiveThresholding(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Adaptive Thresholding'

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
            image_tmp = cv2.cvtColor(image_tmp, cv2.COLOR_BGR2GRAY)
            image_tmp = cv2.medianBlur(image_tmp,5)
            image_tmp = cv2.adaptiveThreshold(image_tmp,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
            image_tmp = cv2.cvtColor(image_tmp, cv2.COLOR_GRAY2BGR)
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret