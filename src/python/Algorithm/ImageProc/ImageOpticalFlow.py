from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np


class ImageOpticalFlow(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Optical Flow'

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
            if self.mLastImage is not None:
                prvs = self.mLastImage[:, :, 0:3]
                hsv = np.zeros_like(prvs)
                prvs = cv2.cvtColor(prvs, cv2.COLOR_BGR2GRAY)
                hsv[..., 1] = 255
                image_tmp = cv2.cvtColor(image_tmp, cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prvs, image_tmp, None, 0.5, 3, 15, 3, 5, 1.2 ,0)
                mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                # x方向：flow[...,0]
                # y方向：flow[...,1]
                hsv[..., 0] = ang*180/np.pi/2
                hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
                image_tmp = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            image[:, :, 0:3] = image_tmp[:, :, :]
            self.mLastImage = image.copy()
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret