from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np



class ImageCornerDetect(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'FAST Corner Detect'

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
            # Initiate FAST object with default values
            fast = cv2.FastFeatureDetector_create()
            # find and draw the keypoints
            kp = fast.detect(image_tmp,None)
            img2 = cv2.drawKeypoints(image_tmp, kp, None, color=(255,0,0))
            image[:, :, 0:3] = img2[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret