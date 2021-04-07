from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np


class ImageFaceDetect(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Face detect'

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
            image_tmp = image_tmp.astype(np.uint8)
            # 人脸识别
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            # 识别眼睛
            eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")
            gray = cv2.cvtColor(image_tmp, cv2.COLOR_BGR2GRAY)
            # 人脸检测
            faces = faceCascade.detectMultiScale(
                gray,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(32, 32)
            )

            result = []
            # 在检测人脸的基础上检测眼睛
            for (x, y, w, h) in faces:
                fac_gray = gray[y: (y+h), x: (x+w)]
                eyes = eyeCascade.detectMultiScale(fac_gray, 1.3, 2)

                # 眼睛坐标的换算，将相对位置换成绝对位置
                for (ex, ey, ew, eh) in eyes:
                    result.append((x+ex, y+ey, ew, eh))

            # 画矩形
            for (x, y, w, h) in faces:
                cv2.rectangle(image_tmp, (x, y), (x+w, y+h), (255, 0, 0), 2)

            for (ex, ey, ew, eh) in result:
                cv2.rectangle(image_tmp, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret