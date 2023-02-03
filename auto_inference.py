import os
import time

import cv2
import numpy as np
import torch

from gui.core.json_settings import Settings
from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh
from utils.torch_utils import select_device


# 自动标注类 我是指针*
class Auto_inference:
    def __init__(self):
        self.pt = None
        self.names = None
        self.stride = None
        self.model = None
        self.device = None
        self.suffix = None
        self.num = 1
        self.im = None
        self.img = None

        # 获取设置
        settings = Settings()
        self.settings = settings.items

        # 模型权重
        self.weights = self.settings['model_path']

        # data数据
        self.data = self.settings['yaml_path']

        # 图片大小
        self.imgsz = (640, 640)

        # 置信度
        self.conf_thres = 0.40
        self.iou_thres = 0.40
        self.classes = None
        self.agnostic_nms = False
        self.max_det = 300

        # 数据集路径
        self.path = self.settings['images_path']

        self.filename = None
        self.file_path = None

        self.load_model()

    # 加载模型
    def load_model(self):
        # 加载模型
        self.device = select_device('')
        self.model = DetectMultiBackend(self.weights, device=self.device, dnn=False, data=self.data, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt

    # 图片推理
    def inference(self):
        last_time = time.time()

        # 将图片传给推理
        self.im = letterbox(self.img, self.imgsz, stride=self.stride, auto=True)[0]  # padded resize
        self.im = self.im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        self.im = np.ascontiguousarray(self.im)  # contiguous

        self.im = torch.from_numpy(self.im).to(self.model.device)
        self.im = self.im.half() if self.model.fp16 else self.im.float()  # uint8 to fp16/32
        self.im /= 255  # 0 - 255 to 0.0 - 1.0

        if len(self.im.shape) == 3:
            self.im = self.im[None]  # expand for batch dim

        # Inference 推理
        pred = self.model(self.im, augment=False, visualize=False)
        # NMS 非极大值抑制
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes,
                                   self.agnostic_nms, max_det=self.max_det)

        labels = ""
        for i, det in enumerate(pred):  # per image
            gn = torch.tensor(self.img.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(self.im.shape[2:], det[:, :4], self.img.shape).round()

                # Write results 写出结果
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    xywh[0] = round(xywh[0], 6)
                    xywh[1] = round(xywh[1], 6)
                    xywh[2] = round(xywh[2], 6)
                    xywh[3] = round(xywh[3], 6)
                    line = (0 if self.names[int(cls)] == "head" else 0, *xywh)  # label format
                    line = str(line).replace(",", "").replace("(", "").replace(")", "") + "\n"
                    labels += line
        # print(labels)
        time_used = str(round((time.time() - last_time) * 1000, 3)) + "ms"
        self.open_labels(suffix=self.suffix, labels=labels, time_used=time_used)

    # 写入标签
    def write_labels(self, labels_file, labels, time_used):
        try:
            print(f"{self.num} 图片 {self.filename} 已推理完成 用时 {time_used}")
            fp = open(labels_file, mode="w", encoding="utf-8")
            fp.write(str(labels))
        except Exception as e:
            print(e)

    # 打开标签文件
    def open_labels(self, filename=None, file_path=None, suffix=None, labels=None, time_used=None):
        if filename and file_path is not None:
            self.filename = filename
            self.file_path = file_path
        # 标签文件
        labels_file = self.file_path[0:self.file_path.find(suffix)] + ".txt"

        # 判断标签文件是否已存在
        if os.path.exists(labels_file):
            # 图片已自动标注
            if labels is not None:
                self.write_labels(labels_file, labels, time_used)
        else:
            # 写入标签文件
            if labels is not None:
                self.write_labels(labels_file, labels, time_used)
            else:
                # 图片未自动标注开始推理
                self.img = cv2.imread(self.file_path)
                self.inference()
                self.num += 1

    # 主函数
    def main(self):
        # 循环获取文件
        self.num = 1
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            suffix = os.path.splitext(file_path)[-1]  # 文件后缀

            # 判断是否为图片
            if suffix == '.jpg' or suffix == '.png' or suffix == '.PNG' \
                    or suffix == '.JPG' or suffix == '.jpeg':
                self.filename = filename
                self.file_path = file_path
                self.suffix = suffix
                self.open_labels(suffix=suffix)
            else:
                if ".txt" not in file_path:
                    print(f"{self.num} 文件 {filename} 不是图片")


# 运行开始
if __name__ == '__main__':
    main = Auto_inference()
    main.main()
