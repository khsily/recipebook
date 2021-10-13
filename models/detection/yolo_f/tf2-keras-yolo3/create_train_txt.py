import glob
from settings import TRAIN_DATASET_PATH


def yolo2bbox(box, img_size):
    img_width, img_height = img_size
    center_x, center_y, box_width, box_height = box
    center_x = center_x * img_height
    center_y = center_y * img_width
    box_width = box_width * img_height
    box_height = box_height * img_width

    x1 = center_x - box_width/2
    y1 = center_y - box_height/2
    x2 = x1 + box_width
    y2 = y1 + box_height

    return int(x1), int(y1), int(x2), int(y2)


data = glob.glob(f'{TRAIN_DATASET_PATH}/*.jpg')
f = open('train.txt', 'w')

for path in data:
    print(path, file=f, end=' ')
    label_path = path.replace('.jpg', '.txt')

    labels = open(label_path, 'r')

    for label in labels.readlines():
        label = label.strip()
        label_split = label.split()

        box = map(float, label_split[1:])
        box = yolo2bbox(box, (416, 416))
        box = list(map(str, box))

        label = ','.join(box + label_split[0:1])
        print(label, file=f, end=' ')

    print(file=f)
    labels.close()

f.close()

print('Done!!!')
