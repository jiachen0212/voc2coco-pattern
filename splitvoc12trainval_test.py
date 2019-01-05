# coding=utf-8
import cv2
import os

allims = '/data2/chenjia/data/voc_coco_pattern/images/JPEGImages'
out = '/data2/chenjia/data/voc_coco_pattern/images/voc2012test'
trainval = '/data2/chenjia/data/VOCdevkit/VOC2012/ImageSets/Main/test.txt'
f = open(trainval)
for line in f:
    im_path = os.path.join(allims, line[:-1] + '.jpg')
    im = cv2.imread(im_path)
    out_path = os.path.join(out, line[:-1] + '.jpg')
    cv2.imwrite(out_path, im)