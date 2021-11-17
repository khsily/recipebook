import os
import random
import shutil

import Image
from PIL import Image


def makedirs(path):
   try:
        os.makedirs(path)
   except OSError:
       if not os.path.isdir(path):
           raise


# path = 'C:/Users/Administrator/PycharmProjects/imgaug/data'
path = 'C:/Users/Administrator/PycharmProjects/imgaug/data_aug'
save_path = 'C:/Users/Administrator/Downloads/val_data'

for name in os.listdir(path):
    f_path = path + '/' + name
    f_file = os.listdir(f_path)
    k1 = [i for i in f_file if i.endswith('.jpg')]
    count = int(len(k1) * 0.1)
    random.seed(1)
    name_jpg = random.sample(k1, count)
    print(name_jpg)
    for jpg in name_jpg:
        copy_path = f_path + '/' + jpg
        print(copy_path)
        # exit()
        save_paths = save_path + '/' + name
        makedirs(save_paths)
        shutil.copy(copy_path, save_paths)

    k2 = [i for i in f_file if i.endswith('.xml')]
    count = int(len(k2) * 0.1)
    random.seed(1)
    name_xml = random.sample(k2, count)
    print(name_xml)
    for xml in name_xml:
        copy_path = f_path + '/' + xml
        save_paths = save_path + '/' + name
        makedirs(save_paths)
        shutil.copy(copy_path, save_paths)
