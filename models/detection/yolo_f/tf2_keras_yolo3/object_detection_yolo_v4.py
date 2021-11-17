import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw
import random
import colorsys

input_size = 416
iou = 0.45
score = 0.25


def read_class_names(class_file_name):
    kor_names = {}
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            kor_name, id_name = name.split(',')
            kor_names[ID] = kor_name.strip('\n')
            names[ID] = id_name.strip('\n')
    return names, kor_names


def draw_bbox(image, bboxes, classes, kor_classes, font_path, show_label=True):
    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    out_boxes, out_scores, out_classes, num_boxes = bboxes
    for i in range(num_boxes[0]):
        if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
        coor = out_boxes[0][i]
        coor[0] = int(coor[0] * image_h)
        coor[2] = int(coor[2] * image_h)
        coor[1] = int(coor[1] * image_w)
        coor[3] = int(coor[3] * image_w)

        fontScale = 0.5
        score = out_scores[0][i]
        class_ind = int(out_classes[0][i])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (int(coor[1]), int(coor[0])), (int(coor[3]), int(coor[2]))
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

        if show_label:
            bbox_mess = '%s: %.2f' % (kor_classes[class_ind], score)

            # 이미지 라벨 그리기
            img_pil = Image.fromarray(image)
            font = ImageFont.truetype(font_path, np.floor(3e-2 * img_pil.size[1] + fontScale).astype('int32'))
            draw = ImageDraw.Draw(img_pil)

            t_size = font.getsize(bbox_mess)
            c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
            draw.rectangle((c1, c3), fill=bbox_color)
            draw.text((c1[0] + 0.1, int(np.float32(c3[1]))), bbox_mess, font=font, fill=(0, 0, 0))

            image = np.array(img_pil)

    return image


def load_model(model_path):
    return keras.models.load_model(model_path)


def predict(model, class_path, image_path, output_path, font_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    image_data = cv2.resize(original_image, (input_size, input_size))
    image_data = image_data / 255.
    image_data = image_data[np.newaxis]

    pred_bbox = model.predict(image_data)

    # 결과같에서 좌표값과 confidence값 분리
    boxes = pred_bbox[:, :, :4]
    pred_conf = pred_bbox[:, :, 4:]

    # nms
    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=iou,
        score_threshold=score
    )

    # 이미지 뿌려주고 저장
    id_classes, kor_classes = read_class_names(class_path)
    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
    image = draw_bbox(original_image, pred_bbox, id_classes, kor_classes, font_path)
    image = Image.fromarray(image.astype(np.uint8))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    cv2.imwrite(output_path, image)

    valid_classes = classes[classes > 0].numpy().astype(int)
    predicted_classes = {kor_classes[key] for key in valid_classes}

    return predicted_classes


if __name__ == '__main__':
    model_path = 'checkpoints/new_model.h5'
    image_path = 'data/test2.jpg'
    output_path = 'result.jpg'
    classes = 'data/classes/recipebook.korean.names'
    font_path = 'font/malgun.ttf'

    model = load_model(model_path)
    res = predict(model, classes, image_path, output_path, font_path)
    print(res)