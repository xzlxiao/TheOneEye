from Algorithm.ImageProc.ImageProcBase import ImageProcBase
import cv2
import numpy as np
from Control import MainController

import time

import torch
from numpy import random
import sys 
sys.path.insert(0, './src/python/Algorithm/yolo')

from Algorithm.yolo.models.experimental import attempt_load
from Algorithm.yolo.utils.datasets import LoadStreams, LoadImages, letterbox
from Algorithm.yolo.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from Algorithm.yolo.utils.plots import plot_one_box
from Algorithm.yolo.utils.torch_utils import select_device, load_classifier, time_synchronized



IMG_SIZE = 640
conf_thres = 0.25 
source = 'data/images'
iou_thres = 0.45

def detect(image: np.array):
    img0 = image
    controller = MainController.getController()
    # Initialize
    device = select_device()
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = controller.mCameraController.mModelYolo  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(IMG_SIZE, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    img = letterbox(img0, imgsz, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = controller.mCameraController.mModelYoloColors

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

    ## main
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model(img, augment=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)

    # Process detections
    for i, det in enumerate(pred):  # detections per image
        im0 = img0
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Write results
            
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'
                im0 = plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
    return im0

class ImageYoloV3(ImageProcBase):
    def __init__(self) -> None:
        super().__init__()
        self.Name = r'YoloV3'

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
            controller = MainController.getController()
            if controller.mCameraController.mModelYolo is not None:
                image_tmp = detect(image_tmp)
            else:
                print('Yolo model is not loaded')
            image[:, :, 0:3] = image_tmp[:, :, :]
            ret = image
        else:
            raise Exception('图像类型不支持')
        return ret