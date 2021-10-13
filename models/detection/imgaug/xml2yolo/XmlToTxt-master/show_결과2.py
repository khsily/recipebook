from matplotlib import pyplot as plt
import cv2
from skimage import io
from os import listdir

path = 'C:/Users/Administrator/PycharmProjects/imgaug/xml2yolo/XmlToTxt-master/out'
img_urls = listdir(path)[0]

image_path = 'C:/Users/Administrator/PycharmProjects/imgaug/xml2yolo/XmlToTxt-master/image'
image_urls = listdir(image_path)[0]


# img_id = '../../../../Desktop/8922_21768_1731.txt'
# image_id = '../../../../Desktop/8922_21768_1731.jpg'
image = 'image'
txt = 'out'
image_list = listdir(image)
txt_list = listdir(txt)
for i, kk in zip(image_list, txt_list):
    k = i
    p = kk
    k = image + '/' + k
    p = txt + '/' + p
    f = open(p, 'r', encoding='utf-8')
    row = f.readline().split(' ')
    f.close()
    img = io.imread(k)
    height, width, channel = img.shape

    print(height, width)
    FileName = row[0]
    left = float(row[1])
    top = float(row[2])
    widths = float(row[3])
    heigths = float(row[4])

    green_color = (0, 255, 0)
    xmin = int(((2*(left*width) - (widths*width))) / 2)
    xmax = int(((2 * left * width) + (widths * width)) / 2)
    ymin = int(((2 * top * height) - (heigths * height)) / 2)
    ymax = int(((2 * top * height) + (heigths * height)) / 2)

    print(f"Coordinates: {xmin, ymin}, {xmax, ymax}")

    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)

    font = cv2.FONT_HERSHEY_SIMPLEX
    plt.figure(figsize=(15, 10))
    plt.title('Image with Bounding Box')
    plt.imshow(img)
    plt.axis("off")
    plt.show()


