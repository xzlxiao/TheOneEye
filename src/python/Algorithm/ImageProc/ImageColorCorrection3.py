from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2 
import numpy as np
from Algorithm.ImageProc.WhiteBalance import *


class ImageColorCorrection3(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Color Correction3'
    
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
            image_tmp = white_balance_3(image_tmp)
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret