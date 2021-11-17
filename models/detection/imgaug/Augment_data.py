import os
import xml.etree.ElementTree as ET
from os import listdir
import cv2
import numpy as np
import imgaug as ia
from imgaug import augmenters as iaa
from pascal_voc_writer import Writer


def makedirs(path):
   try:
        os.makedirs(path)
   except OSError:
       if not os.path.isdir(path):
           raise


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
        if not file.endswith('.xml'):
            images.append(cv2.imread(dir + file, 1))
        else:
            annotation_file = file.replace(file.split('.')[-1], 'xml')
            annotation_file1 = annotation_file.replace('_xml.rf.', '_jpg.rf.')
            # print(annotation_file1)
            bounding_box_list, file_name = read_anntation(dir + annotation_file1)
            annotations.append((bounding_box_list, annotation_file1, file_name))

    images = np.array(images)
    return images, annotations


def augment_x3(list):
    for i in list:
        dir = 'C:/Users/Administrator/PycharmProjects/imgaug/data/{}/'.format(i)
        dirs = 'C:/Users/Administrator/PycharmProjects/imgaug/data_aug/{}/'.format(i)
        makedirs(dirs)
        images, annotations = read_train_dataset(dir)

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
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=90
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r90_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r90_' + annotations[idx][1])
        # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=180
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r180_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r180_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=270
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r270_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r270_' + annotations[idx][1])

def augment_x5(list):
    for i in list:
        dir = 'C:/Users/Administrator/PycharmProjects/imgaug/data/{}/'.format(i)
        dirs = 'C:/Users/Administrator/PycharmProjects/imgaug/data_aug/{}/'.format(i)
        makedirs(dirs)
        images, annotations = read_train_dataset(dir)

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
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=90
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r90_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r90_' + annotations[idx][1])
        # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=180
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r180_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r180_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=270
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r270_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r270_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=95
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r95_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r95_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=115
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r115_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r115_' + annotations[idx][1])

def augment_x10(list):
    for i in list:
        dir = 'C:/Users/Administrator/PycharmProjects/imgaug/data/{}/'.format(i)
        dirs = 'C:/Users/Administrator/PycharmProjects/imgaug/data_aug/{}/'.format(i)
        makedirs(dirs)
        images, annotations = read_train_dataset(dir)

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
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=90
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r90_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r90_' + annotations[idx][1])
        # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=180
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r180_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r180_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=270
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r270_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r270_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=95
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r95_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r95_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=115
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r115_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r115_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=135
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r135_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r135_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=155
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r155_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r155_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=175
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r175_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r175_' + annotations[idx][1])

            # ---------------------------------------------------- #
            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=65
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_65_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_65_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=85
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_85_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_85_' + annotations[idx][1])

def augment_x15(list):
    for i in list:
        dir = 'C:/Users/Administrator/PycharmProjects/imgaug/data/{}/'.format(i)
        dirs = 'C:/Users/Administrator/PycharmProjects/imgaug/data_aug/{}/'.format(i)
        makedirs(dirs)
        images, annotations = read_train_dataset(dir)

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
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=90
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r90_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r90_' + annotations[idx][1])
        # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=180
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r180_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r180_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=270
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r270_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r270_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=95
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r95_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r95_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=115
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r115_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r115_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=135
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r135_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r135_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=155
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r155_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r155_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    rotate=175
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 'r175_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 'r175_' + annotations[idx][1])

            # ---------------------------------------------------- #
            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=65
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_65_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_65_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=85
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_85_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_85_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=95
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_95_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_95_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=115
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_115_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_115_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=135
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_135_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_135_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=155
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r_155_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r_155_' + annotations[idx][1])

            # ---------------------------------------------------- #

            seq = iaa.Sequential([
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 40, "y": 60},
                    scale=(0.5, 0.7),
                    shear=(-16, 16),
                    rotate=175
                )
            ])

            seq_det = seq.to_deterministic()

            image_aug = seq_det.augment_images([image])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            new_image_file = dirs + 's_r175_' + annotations[idx][2]
            cv2.imwrite(new_image_file, image_aug)

            h, w = np.shape(image_aug)[0:2]
            voc_writer = Writer(new_image_file, w, h)
            # exit()
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

            voc_writer.save(dirs + 's_r175_' + annotations[idx][1])


augment_x3(['bacon'])

augment_x5(['id_394','id_1094','id_223','apple','id_2','shrimp','squid','egg_plant','Bean_sprouts','beef','bread','baguette',
            'pork_belly','sweet_potato','id_5','Green_Onion','carrot'])

augment_x10(['tofu', 'egg', 'garlic', 'red_pepper', 'Cheongyang_pepper', 'cucumber'])

augment_x10(['id_726'])
