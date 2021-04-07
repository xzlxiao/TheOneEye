from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2 
import numpy as np


class ImageRotate(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Color Rotate'
        self.mDegree = 70
    
    def process(self, image: np.ndarray) -> np.ndarray:
        rows = image.shape[0]
        cols = image.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,rows/2),self.mDegree,1)
        ret = cv2.warpAffine(image, M, (rows,cols))
        return ret

    def getConfig(self):
        return ('degree', )

    def setConfig(self, config):
        self.mDegree = config['degree']