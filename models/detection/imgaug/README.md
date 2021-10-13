# imgaug

## 유의사항
```
실행할 파일의 주소를 수정할것
```
## 1번 작업
```
imgaug/data에 사진과 라벨링된(xml) 파일을 저장한다.  
```
## 2번 작업
```
Augment_data.py를 실행 한다.
```
## 3번 작업(xml2yolo)
```
xml2yolo/XmlToTxt-master/classes.txt를 수정한다.
```
## 4번 작업
```
cd ../../imgaug/xml2yolo/XmlToTxt-master
```
## 5번 작업
```
python xmltotxt.py -c classes.txt -xml xml -out out
```