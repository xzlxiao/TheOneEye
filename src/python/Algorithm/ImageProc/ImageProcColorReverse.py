from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2 
import numpy as np


class ImageProcColorReverse(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Color Reverse'
    
    def process(self, image: np.ndarray) -> np.ndarray:
        ret = super().process(image)
        # print(self.channels(image))
        if self.channels(image)==1:
            height,width = image.shape
            for i in range(height):
                for j in range(width):
                    ret[i,j] = (255-image[i,j]) 
        elif self.channels(image)==3:
            ret = 255-image
        elif self.channels(image)==4:
            image_tmp = image[:, :, 0:3]
            image_tmp = 255 - image_tmp
            image[:, :, 0:3] = image_tmp[:,:,:]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret