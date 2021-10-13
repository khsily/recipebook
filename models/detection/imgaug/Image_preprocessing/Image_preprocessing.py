from PIL import Image
from os import listdir

path = 'C:/Users/Administrator/Desktop/yolo_data'
save_path = 'C:/Users/Administrator/Desktop/yolo_save'
f_list = listdir(path)
print(f_list)
exit()
for i in f_list:
    image_paths = listdir(path + '/' + i)
    # print(image_paths)
    # print(image_paths[1])
    # exit()
    count = 1
    for k in range(len(image_paths)):
        image_name = image_paths[k]
        print(image_name)
        # exit()
        image = Image.open(path + '/' + i + '/' + image_name)
        resize_image = image.resize((416, 416))
        resize_image.save(save_path + '/' + i + '/' + f'{i}_{count}.jpg')
        count += 1
