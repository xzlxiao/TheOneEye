from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np


class ImageKmean8(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'K-mean 8'

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
            Z = image_tmp.reshape((-1,3))
            # convert to np.float32
            Z = np.float32(Z)
            # define criteria, number of clusters(K) and apply kmeans()
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            K = 8
            ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
            # Now convert back into uint8, and make original image
            center = np.uint8(center)
            res = center[label.flatten()]
            image_tmp = res.reshape((image_tmp.shape))
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret