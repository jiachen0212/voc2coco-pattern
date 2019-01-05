# coding=utf-8
import xml.etree.ElementTree as ET
import os
import json


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
    sig_xml_box = []
    tree = ET.parse(xmlname)
    root = tree.getroot()
    images = {}
    for i in root:  # 遍历一级节点
        if i.tag == 'filename':
            file_name = i.text  # 0001.jpg
            # print('image name: ', file_name)
            images['file_name'] = file_name
        if i.tag == 'size':
            for j in i:
                if j.tag == 'width':
                    width = j.text
                    images['width'] = int(width)
                if j.tag == 'height':
                    height = j.text
                    images['height'] = int(height)
        if i.tag == 'object':
            cat_id = 0
            for j in i:
                if j.tag == 'name':
                    cls_name = j.text
                    cat_id = voc_clses.index(cls_name) + 1
                if j.tag == 'bndbox':
                    bbox = []
                    xmin = 0
                    ymin = 0
                    xmax = 0
                    ymax = 0
                    for r in j:
                        if r.tag == 'xmin':
                            xmin = eval(r.text)
                        if r.tag == 'ymin':
                            ymin = eval(r.text)
                        if r.tag == 'xmax':
                            xmax = eval(r.text)
                        if r.tag == 'ymax':
                            ymax = eval(r.text)
                    bbox.append(xmin)
                    bbox.append(ymin)
                    bbox.append(xmax - xmin)
                    bbox.append(ymax - ymin)
                    bbox.append(id)   # 保存当前box对应的image_id
                    bbox.append(cat_id)
                    sig_xml_box.append(bbox)
                    # print('bbox', xmin, ymin, xmax - xmin, ymax - ymin, 'id', id, 'cls_id', cat_id)
    images['id'] = id
    # print ('sig_img_box', sig_xml_box)
    return images, sig_xml_box



def txt2list(txtfile):
    f = open(txtfile)
    l = []
    for line in f:
        l.append(line[:-1])
    return l


# voc2007xmls = 'anns'
voc2007xmls = '/data2/chenjia/data/VOCdevkit/VOC2007/Annotations'
# test_txt = 'voc2007/test.txt'
test_txt = '/data2/chenjia/data/VOCdevkit/VOC2007/ImageSets/Main/test.txt'
xml_names = txt2list(test_txt)
xmls = []
bboxes = []
ann_js = {}
for ind, xml_name in enumerate(xml_names):
    xmls.append(os.path.join(voc2007xmls, xml_name + '.xml'))
json_name = 'instances_voc2007val.json'
images = []
for i_index, xml_file in enumerate(xmls):
    image, sig_xml_bbox = getimages(xml_file, i_index)
    images.append(image)
    bboxes.extend(sig_xml_bbox)
ann_js['images'] = images
ann_js['categories'] = categories
annotations = []
for box_ind, box in enumerate(bboxes):
    anno = {}
    anno['image_id'] = box[-2]
    anno['category_id'] = box[-1]
    anno['bbox'] = box[:-2]
    anno['id'] = box_ind + 1
    anno['iscrowd'] = 0
    annotations.append(anno)
ann_js['annotations'] = annotations
json.dump(ann_js, open(json_name, 'w'), indent=4)  # indent=4 更加美观显示

