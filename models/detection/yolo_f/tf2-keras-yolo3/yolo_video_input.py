import argparse
from yolo import YOLO, detect_video
from PIL import Image


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' +
        YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' +
        YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' +
        YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' +
        str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='./path2your_video',
        help="Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help="[Optional] Video output path"
    )
    #
    model_pt = 'log/000/ep056-loss10.202-val_loss10.101.h5'
    inp = 'test/chives_8s.jpg'

    FLAGS = parser.parse_args()

    while True:
        try:
            yolo = YOLO(**vars(FLAGS))
            image_input = str(input("식재료를 구분할 이미지를 이름을 입력해 주세요 : "))
            if image_input != '끝':
                image_path = 'test/' + image_input
                image = Image.open(image_path)
                print("Image detection mode")
                r_image, name, in_name = yolo.detect_image(image)
                print(name)
                print(in_name)
                image.save(f'save_image/{in_name}.jpg')
                r_image.show()
                print('save_image 폴더에 저장되었습니다')
                print('다른 파일도 하시겠습니까?')
                print('끝 내리시려면 끝이라 입력해 주세요')
            else:
                break
        except:
            print("이미지 파일이 없습니다.")



