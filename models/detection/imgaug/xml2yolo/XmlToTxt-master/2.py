from matplotlib import pyplot as plt
import cv2
from skimage import io
from os import listdir

path = 'C:/Users/Administrator/PycharmProjects/imgaug/xml2yolo/XmlToTxt-master/out'
img_urls = listdir(path)[0]

image_path = 'C:/Users/Administrator/PycharmProjects/imgaug/xml2yolo/XmlToTxt-master/image'
image_urls = listdir(image_path)[0]


img_id = 'C:/Users/Administrator/PycharmProjects/imgaug/xml2yolo/XmlToTxt-master/out/raccoon-1_jpg.rf.4735f8b019bd0bfa86593b474aa7a5fa.txt'
image_id = 'C:/Users/Administrator/PycharmProjects/imgaug/xml2yolo/XmlToTxt-master/image/raccoon-1_jpg.rf.4735f8b019bd0bfa86593b474aa7a5fa.jpg'
# print(img_urls)
k = image_id
p = img_id
f = open(p, 'r', encoding='utf-8')
row = f.readline().split(' ')
f.close()
img = io.imread(k)
# print(img)
# exit()
height, width, channel = img.shape
print(height, width)
# exit()
FileName = row[0]
box = row
left = float(box[1])
top = float(box[2])
width = float(box[3])
height = float(box[4])
# labels_to_names 딕셔너리로 class_id값을 클래스명으로 변경. opencv에서는 class_id + 1로 매핑해야함.
# caption = "{}: {:.4f}".format(labels_to_names_seq[class_ids[i]], confidences[i])
#cv2.rectangle()은 인자로 들어온 draw_img에 사각형을 그림. 위치 인자는 반드시 정수형.
green_color = (0, 255, 0)
red_color = (0, 0, 255)
cv2.rectangle(img, (int(left), int(top)), (int(left+width), int(top+height)), color=green_color, thickness=2)
# cv2.putText(img, (int(left), int(top - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red_color, 1)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(12, 12))
plt.imshow(img_rgb)


