from Algorithm.ImageProc.ImageProcBase import ImageProcBase
from PyQt5.QtWidgets import QLabel, QFrame, QMenu, QAction, QGridLayout, QInputDialog, QDialog
from PyQt5.QtGui import QImage
import cv2 
import numpy as np
from Common.Common import Common
import cv2
from PIL import Image
import copy


class ImageSave(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'Image Save'
    
    def process(self, image: np.ndarray) -> np.ndarray:
        ret = super().process(image)
        # print(self.channels(image))
        # ret = copy.deepcopy(image)
        TURN = cv2.cvtColor(ret, cv2.COLOR_BGR2RGB)
        save_image = Image.fromarray(TURN)
        saveDir = self.mImageSaveDir
        save_name = saveDir + '/image_' + Common.getDirTime() + '.png'
        Common.mkdir(saveDir)
        # if not cv2.imwrite(save_name, ret):
        #     print('保存失败：' + save_name)
        # else:
        #     pass
        # save_image.show()
        save_image.save(save_name, 'png')
        return ret