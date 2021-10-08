import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import random
from skimage import io
from shutil import copyfile
import sys
import time
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array


images_boxable_fname = 'train-images-boxable-with-rotation.csv'
annotations_bbox_fname = 'train-annotations-bbox.csv'
class_descriptions_fname = 'class-descriptions-boxable.csv'

images_boxable = pd.read_csv(images_boxable_fname)
annotations_bbox = pd.read_csv(annotations_bbox_fname)
class_descriptions = pd.read_csv(class_descriptions_fname, header=None)


# print(images_boxable.head())
# annotations_bbox.head()
# class_descriptions.head()


def plot_bbox(img_id):
  img_url = images_boxable.loc[images_boxable["ImageID"]==img_id]['OriginalURL'].values[0]
  img = io.imread(img_url)
  height, width, channel = img.shape
  print(f"Image: {img.shape}")
  bboxs = annotations_bbox[annotations_bbox['ImageID']==img_id]
  for index, row in bboxs.iterrows():
      xmin = row['XMin']
      xmax = row['XMax']
      ymin = row['YMin']
      ymax = row['YMax']
      xmin = int(xmin*width)
      xmax = int(xmax*width)
      ymin = int(ymin*height)
      ymax = int(ymax*height)
      label_name = row['LabelName']
      class_series = class_descriptions[class_descriptions[0]==label_name]
      class_name = class_series[1].values[0]
      print(f"Coordinates: {xmin,ymin}, {xmax,ymax}")
      cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (255,0,0), 5)
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(img, class_name, (xmin,ymin-10), font, 3, (0,255,0), 5)
  plt.figure(figsize=(15,10))
  plt.title('Image with Bounding Box')
  plt.imshow(img)
  plt.axis("off")
  plt.show()

least_objects_img_ids = annotations_bbox["ImageID"].value_counts().tail(50).index.values
# for img_id in random.sample(list(least_objects_img_ids), 5):
  # plot_bbox(img_id)

# exit()


print(class_descriptions.loc[class_descriptions[1].isin(['Person', 'Mobile phone', 'Car'])])

person_pd = class_descriptions[class_descriptions[1]=='Person']
phone_pd = class_descriptions[class_descriptions[1]=='Mobile phone']
car_pd = class_descriptions[class_descriptions[1]=='Car']
Magpie_pd = class_descriptions[class_descriptions[1]=='Magpie']


label_name_person = person_pd[0].values[0]
label_name_phone = phone_pd[0].values[0]
label_name_car = car_pd[0].values[0]
label_name_Magpie = Magpie_pd[0].values[0]


person_bbox = annotations_bbox[annotations_bbox['LabelName']==label_name_person]
phone_bbox = annotations_bbox[annotations_bbox['LabelName']==label_name_phone]
car_bbox = annotations_bbox[annotations_bbox['LabelName']==label_name_car]
Magpie_bbox = annotations_bbox[annotations_bbox['LabelName']==label_name_Magpie]


print('There are %d persons in the dataset' %(len(person_bbox)))
print('There are %d phones in the dataset' %(len(phone_bbox)))
print('There are %d cars in the dataset' %(len(car_bbox)))
print('There are %d Magpie_bbox in the dataset' %(len(Magpie_bbox)))

person_img_id = person_bbox['ImageID']
phone_img_id = phone_bbox['ImageID']
car_img_id = car_bbox['ImageID']
Magpie_img_id = Magpie_bbox['ImageID']


person_img_id = np.unique(person_img_id)
phone_img_id = np.unique(phone_img_id)
car_img_id = np.unique(car_img_id)
Magpie_img_id = np.unique(Magpie_img_id)

print('There are %d images which contain persons' % (len(person_img_id)))
print('There are %d images which contain phones' % (len(phone_img_id)))
print('There are %d images which contain cars' % (len(car_img_id)))
print('There are %d images which contain cars' % (len(Magpie_img_id)))

n = 10
subperson_img_id = random.sample(list(person_img_id), n)
subphone_img_id = random.sample(list(phone_img_id), n)
subcar_img_id = random.sample(list(car_img_id), n)
subMagpie_img_id = random.sample(list(Magpie_img_id), n)


subperson_pd = images_boxable.loc[images_boxable['ImageID'].isin(subperson_img_id)]
subphone_pd = images_boxable.loc[images_boxable['ImageID'].isin(subphone_img_id)]
subcar_pd = images_boxable.loc[images_boxable['ImageID'].isin(subcar_img_id)]
subMagpie_pd = images_boxable.loc[images_boxable['ImageID'].isin(subMagpie_img_id)]


print(subperson_pd.shape)
print(subMagpie_pd.shape)

print(subperson_pd.head())

subperson_dict = subperson_pd[["ImageID", "OriginalURL"]].set_index('ImageID')["OriginalURL"].to_dict()
subphone_dict = subphone_pd[["ImageID", "OriginalURL"]].set_index('ImageID')["OriginalURL"].to_dict()
subcar_dict = subcar_pd[["ImageID", "OriginalURL"]].set_index('ImageID')["OriginalURL"].to_dict()
subMagpie_dict = subMagpie_pd[["ImageID", "OriginalURL"]].set_index('ImageID')["OriginalURL"].to_dict()

# mappings = [subperson_dict, subphone_dict, subcar_dict]
mappings = [subperson_dict, subphone_dict, subcar_dict, subMagpie_dict]

print(len(mappings))
print(len(mappings[0]))

classes = ['Person', 'Mobile phone', 'Car', 'Magpie']


# download images
def just_one():
  for idx, obj_type in enumerate(classes):
    n_issues = 0
    # create the directory
    if not os.path.exists(obj_type):
      os.mkdir(obj_type)
    for img_id, url in mappings[idx].items():
      try:
        img = io.imread(url)
        saved_path = os.path.join(obj_type, img_id+".jpg")
        io.imsave(saved_path, img)
      except Exception as e:
        n_issues += 1
    print(f"Images Issues: {n_issues}")

just_one()


train_path = 'train'
test_path = 'test'

random.seed(1)

for i in range(len(classes)):
    all_imgs = os.listdir(classes[i])
    all_imgs = [f for f in all_imgs if not f.startswith('.')]
    random.shuffle(all_imgs)

    limit = int(n * 0.8)

    train_imgs = all_imgs[:limit]
    test_imgs = all_imgs[limit:]

    # copy each classes' images to train directory
    for j in range(len(train_imgs)):
        original_path = os.path.join(classes[i], train_imgs[j])
        new_path = os.path.join(train_path, train_imgs[j])
        copyfile(original_path, new_path)

    # copy each classes' images to test directory
    for j in range(len(test_imgs)):
        original_path = os.path.join(classes[i], test_imgs[j])
        new_path = os.path.join(test_path, test_imgs[j])
        copyfile(original_path, new_path)

label_names = [label_name_person, label_name_phone, label_name_car, label_name_Magpie]
train_df = pd.DataFrame(columns=['FileName', 'XMin', 'XMax', 'YMin', 'YMax', 'ClassName'])

# Find boxes in each image and put them in a dataframe
train_imgs = os.listdir(train_path)
train_imgs = [name for name in train_imgs if not name.startswith('.')]

for i in range(len(train_imgs)):
    sys.stdout.write('Parse train_imgs ' + str(i) + '; Number of boxes: ' + str(len(train_df)) + '\r')
    sys.stdout.flush()
    img_name = train_imgs[i]
    img_id = img_name[0:16]
    tmp_df = annotations_bbox[annotations_bbox['ImageID']==img_id]
    for index, row in tmp_df.iterrows():
        labelName = row['LabelName']
        for i in range(len(label_names)):
            if labelName == label_names[i]:
                train_df = train_df.append({'FileName': img_name,
                                            'XMin': row['XMin'],
                                            'XMax': row['XMax'],
                                            'YMin': row['YMin'],
                                            'YMax': row['YMax'],
                                            'ClassName': classes[i]},
                                           ignore_index=True)
                train_df.to_csv('train.csv')


print(train_df.head())
print(train_df.shape)

train_img_ids = train_df["FileName"].head().str.split(".").str[0].unique()
# for img_id in train_img_ids:
#   plot_bbox(img_id)

test_df = pd.DataFrame(columns=['FileName', 'XMin', 'XMax', 'YMin', 'YMax', 'ClassName'])

# Find boxes in each image and put them in a dataframe
test_imgs = os.listdir(test_path)
test_imgs = [name for name in test_imgs if not name.startswith('.')]

for i in range(len(test_imgs)):
    sys.stdout.write('Parse train_imgs ' + str(i) + '; Number of boxes: ' + str(len(test_df)) + '\r')
    sys.stdout.flush()
    img_name = test_imgs[i]
    img_id = img_name[0:16]
    tmp_df = annotations_bbox[annotations_bbox['ImageID']==img_id]
    for index, row in tmp_df.iterrows():
        labelName = row['LabelName']
        for i in range(len(label_names)):
            if labelName == label_names[i]:
                test_df = test_df.append({'FileName': img_name,
                                            'XMin': row['XMin'],
                                            'XMax': row['XMax'],
                                            'YMin': row['YMin'],
                                            'YMax': row['YMax'],
                                            'ClassName': classes[i]},
                                           ignore_index=True)
                test_df.to_csv('test.csv')

print(test_df.head())
print(test_df.shape)




# for training
# exit()
with open("annotation.txt", "w+") as f:
    for idx, row in train_df.iterrows():
        img = cv2.imread('train/' + row['FileName'])
        height, width = img.shape[:2]
        x1 = int(row['XMin'] * width)
        x2 = int(row['XMax'] * width)
        y1 = int(row['YMin'] * height)
        y2 = int(row['YMax'] * height)

        google_colab_file_path = 'C:\\Users\\Administrator\\PycharmProjects\\test4\\train'
        fileName = os.path.join(google_colab_file_path, row['FileName'])
        className = row['ClassName']
        f.write(fileName + ',' + str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2) + ',' + className + '\n')

test_df = pd.read_csv('test.csv')

# for test
with open("test_annotation.txt", "w+") as f:
    for idx, row in test_df.iterrows():
        sys.stdout.write(str(idx) + '\r')
        sys.stdout.flush()
        img = cv2.imread('test/' + row['FileName'])
        height, width = img.shape[:2]
        x1 = int(row['XMin'] * width)
        x2 = int(row['XMax'] * width)
        y1 = int(row['YMin'] * height)
        y2 = int(row['YMax'] * height)

        google_colab_file_path = 'C:\\Users\\Administrator\\PycharmProjects\\test4\\test'
        fileName = os.path.join(google_colab_file_path, row['FileName'])
        className = row['ClassName']
        f.write(fileName + ',' + str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2) + ',' + className + '\n')\

