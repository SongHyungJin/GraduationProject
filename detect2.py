#-*- encoding: utf8 -*-
import os
import sys
from pathlib import Path
import glob
import torch
import numpy as np
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, cv2, check_file, check_img_size, check_requirements,
                           non_max_suppression, scale_coords)
from utils.plots import save_one_box
from utils.torch_utils import time_sync


@torch.no_grad()
def detectNcut(src, dst, detectType, weights=str('models/best5l.pt'), data=str('models/test.yaml')):
    file_list = [[], []]
    file_list2 = []
    # weights = [str('models/best5l.pt')]  # model.pt path(s)
    # data = str('models/test.yaml')  # dataset.yaml path
    imgsz = (640, 640)  # inference size (height, width)
    conf_thres = 0.25  # confidence threshold
    iou_thres = 0.45  # NMS IOU threshold
    max_det = 1000  # maximum detections per image
    classes = None  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms = False  # class-agnostic NMS
    augment = False  # augmented inference
    half = False  # use FP16 half-precision inference
    dnn = False  # use OpenCV DNN for ONNX inference

    source = str(src)
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    if is_url and is_file:
        source = check_file(source)  # download

    # Load model
    device = torch.device('cpu')
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    if webcam:
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
    for path, im, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(im, augment=augment, visualize=False)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            s += '%gx%g ' % im.shape[2:]  # print string
            imc = im0.copy()  # for save_crop
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    if c == 0 and detectType == 1:  # head일때만 저장 나중에 yolo모델 수정하고 여기도 갱신할것 물건 detect일때는 굳이 저장하지 않게 수정
                        save_one_box(xyxy, imc, file=Path(dst + '/' + str(names[c]) + '/' + str(p.stem) + '.jpg'),
                                     BGR=True, square=True)
                        file_list[0].append(os.path.join(path))
                        file_list[1].append(os.path.join(dst + '/' + str(names[c]) + '/' + str(p.stem) + '.jpg'))
                    elif detectType == 0:
                        file_list2.append(os.path.join(path))

        LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

    if detectType == 1:
        return file_list
    else:
        return file_list2



# detectNcut('C:/Users/kjma8y/Downloads/과제/학습용/chara/mayu_new', 'C:/Users/kjma8y/Downloads/과제/학습용/chara/mayu_new')

