import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np
import sys 
sys.path.append('/home/xzlxiao/Code/research/TheOneEye/src/python')
sys.path.append('/home/xzlxiao/Code/research/TheOneEye')
from Algorithm.yolo.models.experimental import attempt_load
from Algorithm.yolo.utils.datasets import LoadStreams, LoadImages, letterbox
from Algorithm.yolo.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from Algorithm.yolo.utils.plots import plot_one_box
from Algorithm.yolo.utils.torch_utils import select_device, load_classifier, time_synchronized
WEIGHTS = '/home/data/yolov3.pt'

IMG_SIZE = 640
conf_thres = 0.25 
source = 'data/images'
iou_thres = 0.45

def detect(image: np.array):
    img0 = image

    # Initialize
    

    
    set_logging()
    device = select_device()
    half = device.type != 'cpu'  # half precision only supported on CUDA
    # Load model
    model = attempt_load(WEIGHTS, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(IMG_SIZE, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    img = letterbox(img0, imgsz, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    
    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    
    t0 = time.time()

    ## main
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    print(img.shape)
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
                plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

    print(f'Done. ({time.time() - t0:.3f}s)')
    return im0


if __name__ == '__main__':
    check_requirements(exclude=('pycocotools', 'thop'))
    image = cv2.imread('/home/xzlxiao/下载/03a1e44178dfe67efbe518b4d781ef00.jpeg') 
    ret = None

    with torch.no_grad():
        ret = detect(image)
    
    print(ret.shape)
    cv2.imshow('test', ret)
    cv2.waitKey()