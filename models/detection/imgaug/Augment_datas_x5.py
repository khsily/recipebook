import xml.etree.ElementTree as ET
from os import listdir
import cv2
import numpy as np
import imgaug as ia
from imgaug import augmenters as iaa
from pascal_voc_writer import Writer


def read_anntation(xml_file: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    bounding_box_list = []

    file_name = root.find('filename').text
    for obj in root.iter('object'):

        object_label = obj.find("name").text
        for box in obj.findall("bndbox"):
            x_min = int(box.find("xmin").text)
            y_min = int(box.find("ymin").text)
            x_max = int(box.find("xmax").text)
            y_max = int(box.find("ymax").text)

        bounding_box = [object_label, x_min, y_min, x_max, y_max]
        bounding_box_list.append(bounding_box)

    return bounding_box_list, file_name


def read_train_dataset(dir):
    images = []
    annotations = []
    for file in listdir(dir):
        # print(file)
        if file.endswith('.jpg'):
            images.append(cv2.imread(dir + file, 1))
        else:
            annotation_file = file.replace(file.split('.')[-1], 'xml')
            annotation_file1 = annotation_file.replace('_xml.rf.', '_jpg.rf.')
            # print(annotation_file1)
            bounding_box_list, file_name = read_anntation(dir + annotation_file1)
            annotations.append((bounding_box_list, annotation_file1, file_name))

    images = np.array(images)
    return images, annotations


dir = 'C:/Users/hancom/PycharmProjects/recipebook/models/detection/imgaug/imgaug/data/'
images, annotations = read_train_dataset(dir)
# read_train_dataset(dir)

for idx in range(len(images)):
    image = images[idx]
    boxes = annotations[idx][0]
    print(image)
    print(boxes)
    # exit()
    ia_bounding_boxes = []
    for box in boxes:
        ia_bounding_boxes.append(ia.BoundingBox(x1=box[1], y1=box[2], x2=box[3], y2=box[4]))
    print(ia_bounding_boxes)
    bbs = ia.BoundingBoxesOnImage(ia_bounding_boxes, shape=image.shape)

    seq = iaa.Sequential([
        iaa.Multiply((1.2, 1.5)),
        iaa.Affine(
            rotate=90,
        )
    ])

    seq_det = seq.to_deterministic()

    image_aug = seq_det.augment_images([image])[0]
    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

    new_image_file = dir + 'r90_' + annotations[idx][2]
    cv2.imwrite(new_image_file, image_aug)

    h, w = np.shape(image_aug)[0:2]
    voc_writer = Writer(new_image_file, w, h)
    # exit()
    for i in range(len(bbs_aug.bounding_boxes)):
        bb_box = bbs_aug.bounding_boxes[i]
        voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

    voc_writer.save(dir + 'r90_' + annotations[idx][1])

    # ---------------------------------------------------- #

    seq = iaa.Sequential([
        iaa.Multiply((1.2, 1.5)),
        iaa.Affine(
            rotate=180
        )
    ])

    seq_det = seq.to_deterministic()

    image_aug = seq_det.augment_images([image])[0]
    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

    new_image_file = dir + 'r180_' + annotations[idx][2]
    cv2.imwrite(new_image_file, image_aug)

    h, w = np.shape(image_aug)[0:2]
    voc_writer = Writer(new_image_file, w, h)
    # exit()
    for i in range(len(bbs_aug.bounding_boxes)):
        bb_box = bbs_aug.bounding_boxes[i]
        voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

    voc_writer.save(dir + 'r180_' + annotations[idx][1])

    # ---------------------------------------------------- #

    seq = iaa.Sequential([
        iaa.Multiply((1.2, 1.5)),
        iaa.Affine(
            rotate=270
        ),
        # iaa.ImpulseNoise(0.1)
    ])

    seq_det = seq.to_deterministic()

    image_aug = seq_det.augment_images([image])[0]
    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

    new_image_file = dir + 'r270_' + annotations[idx][2]
    cv2.imwrite(new_image_file, image_aug)

    h, w = np.shape(image_aug)[0:2]
    voc_writer = Writer(new_image_file, w, h)
    # exit()
    for i in range(len(bbs_aug.bounding_boxes)):
        bb_box = bbs_aug.bounding_boxes[i]
        voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

    voc_writer.save(dir + 'r270_' + annotations[idx][1])
    # ---------------------------------------------------- #

    # ---------------------------------------------------- #

    seq = iaa.Sequential([
        iaa.Multiply((1.2, 1.5)),
        iaa.Affine(
            rotate=270
        ),
        iaa.ImpulseNoise(0.1)
    ])

    seq_det = seq.to_deterministic()

    image_aug = seq_det.augment_images([image])[0]
    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

    new_image_file = dir + 'r_n_270_' + annotations[idx][2]
    cv2.imwrite(new_image_file, image_aug)

    h, w = np.shape(image_aug)[0:2]
    voc_writer = Writer(new_image_file, w, h)
    # exit()
    for i in range(len(bbs_aug.bounding_boxes)):
        bb_box = bbs_aug.bounding_boxes[i]
        voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

    voc_writer.save(dir + 'r_n_270_' + annotations[idx][1])
    # ---------------------------------------------------- #

    # ---------------------------------------------------- #

    seq = iaa.Sequential([
        iaa.Multiply((1.2, 1.5)),
        iaa.Affine(
            rotate=90
        ),
        iaa.ImpulseNoise(0.1)
    ])

    seq_det = seq.to_deterministic()

    image_aug = seq_det.augment_images([image])[0]
    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

    new_image_file = dir + 'r_n_90_' + annotations[idx][2]
    cv2.imwrite(new_image_file, image_aug)

    h, w = np.shape(image_aug)[0:2]
    voc_writer = Writer(new_image_file, w, h)
    # exit()
    for i in range(len(bbs_aug.bounding_boxes)):
        bb_box = bbs_aug.bounding_boxes[i]
        voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

    voc_writer.save(dir + 'r_n_90_' + annotations[idx][1])
    # ---------------------------------------------------- #
