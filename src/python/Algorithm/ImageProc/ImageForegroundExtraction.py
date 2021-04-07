from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np


class ImageForegroundExtraction(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Foreground Extraction using GrabCut'

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
            mask = np.zeros(image_tmp.shape[:2],np.uint8)
            bgdModel = np.zeros((1,65),np.float64)
            fgdModel = np.zeros((1,65),np.float64)
            rect = (50,50,450,290)
            cv2.grabCut(image_tmp,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
            image_tmp = image_tmp*mask2[:,:,np.newaxis]
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret