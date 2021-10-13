# -*- coding: utf-8 -*-
# @Time    : 2020/6/29 14:13
# @Author  : AaronJny
# @File    : settings.py
# @Desc    :

TRAIN_DATASET_PATH = 'dataset'  # 바꾸기
# DEFAULT_MODEL_PATH = 'logs/000/trained_weights_final.h5'  # 바꾸기
DEFAULT_MODEL_PATH = 'logs/000/ep056-loss8.532-val_loss8.528.h5'  # 바꾸기
DEFAULT_ANCHORS_PATH = 'model_data/yolo_anchors.txt'
DEFAULT_CLASSES_PATH = 'model_data/coco_classes.txt'  # 바꾸기

# 模型置信度阈值，低于阈值的box将被忽略
SCORE = 0.3
# IOU阈值
IOU = 0.45
# 模型默认图片大小，如果你不清楚这一项的实际用途，请千万不要修改它
MODEL_IMAGE_SIZE = (416, 416)
# GPU数量
GPU_NUM = 1
# 训练数据路径，其格式参考README.MD
TRAIN_DATA_PATH = 'train.txt'
# 验证集比例
VALID_SPLIT = 0.1
# 是否开启图像增广
IMAGE_AUGMENTATION = True
# 训练日志、输出目录
LOGS_DIR = 'logs/000/'
# 预训练的TINY YOLO模型权重路径
PRE_TRAINING_TINY_YOLO_WEIGHTS = 'model_data/tiny_yolo_weights.h5'
# 预训练的YOLO模型权重路径
PRE_TRAINING_YOLO_WEIGHTS = 'model_data/darknet53_weights.h5'
# 训练阶段1开关-冻结大多数层训练，获得一个相对稳定的模型
FROZEN_TRAIN = False
# 训练阶段1的学习率
FROZEN_TRAIN_LR = 1e-3
# 阶段1的batch size
FROZEN_TRAIN_BATCH_SIZE = 32
# 阶段1模型权重输出路径，填写`相较于LOGS_DIR的相对路径`或者`绝对路径`
FROZEN_TRAIN_OUTPUT_WEIGHTS = 'trained_weights_stage_1.h5'
# 训练阶段2开关-解冻所有层，进行fine-turn
UNFREEZE_TRAIN = True
# 阶段2初始学习率
UNFREEZE_TRAIN_LR = 1e-4
# 阶段2的batch size，建议设小一点，大了可能会OOM
UNFREEZE_TRAIN_BATCH_SIZE = 4
# 阶段2模型权重输出路径，填写`相较于LOGS_DIR的相对路径`或者`绝对路径`
UNFREEZE_TRAIN_OUTPUT_WEIGHTS = 'trained_weights_stage_2.h5'
# 最终模型权重输出路径，填写`相较于LOGS_DIR的相对路径`或者`绝对路径`
FINAL_OUTPUT_WEIGHTS = 'trained_weights_final.h5'
