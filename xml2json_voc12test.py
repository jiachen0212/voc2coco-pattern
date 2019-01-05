# coding=utf-8
import xml.etree.ElementTree as ET
import os
import json
import cv2


voc_clses = ['aeroplane', 'bicycle', 'bird', 'boat',
    'bottle', 'bus', 'car', 'cat', 'chair',
    'cow', 'diningtable', 'dog', 'horse',
    'motorbike', 'person', 'pottedplant',
    'sheep', 'sofa', 'train', 'tvmonitor']


categories = []
for iind, cat in enumerate(voc_clses):
    cate = {}
    cate['supercategory'] = cat
    cate['name'] = cat
    cate['id'] = iind + 1
    categories.append(cate)

def getimages(xmlname, id):
    images = {}
    im = cv2.imread(xmlname)
    height, width = im.shape[:2]
    images['file_name'] = xmlname.split('/')[-1]
    images['height'] = height
    images['width'] = width
    images['id'] = id
    print (images['file_name'])
    return images



def txt2list(txtfile):
    f = open(txtfile)
    l = []
    for line in f:
        l.append(line[:-1])
    return l


# voc2007xmls = 'anns'
voc2012ims = '/data2/chenjia/data/VOCdevkit/VOC2012/JPEGImages'
# test_txt = 'voc2007/test.txt'
test_txt = '/data2/chenjia/data/VOCdevkit/VOC2012/ImageSets/Main/test.txt'
xml_names = txt2list(test_txt)
ims = []
bboxes = []
ann_js = {}
for ind, xml_name in enumerate(xml_names):
    ims.append(os.path.join(voc2012ims, xml_name + '.jpg'))
json_name = 'instances_voc2012test.json'
images = []
for i_index, im_file in enumerate(ims):
    image = getimages(im_file, i_index)
    images.append(image)
    # bboxes.extend(sig_xml_bbox)
ann_js['images'] = images
ann_js['categories'] = categories
# annotations = []
# for box_ind, box in enumerate(bboxes):
#     anno = {}
#     anno['image_id'] =  box[-2]
#     anno['category_id'] = box[-1]
#     anno['bbox'] = box[:-2]
#     anno['id'] = box_ind
#     annotations.append(anno)
# ann_js['annotations'] = annotations
json.dump(ann_js, open(json_name, 'w'), indent=4)  # indent=4 更加美观显示

