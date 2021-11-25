# 프로젝트 레시피북

<img src="./images/hamster.png" width='300px' />

한컴 아카데미 딥러닝 교육과정 파이널 프로젝트. Project Recipebook
<br/><br/>


## 프로젝트 구조
```
.
├── client              : React Native 기반 Android/IOS 어플리케이션
├── database            : postgresql 기반 데이터베이스
├── models
│   ├── detection       : 식재료 인식 모델
│   └── recommenders    : 레시피 추천 모델 (NeuMF)
└── server              : Flask 기반 Rest-api 서버
```

## Getting Started
1. 프로젝트 루트에 .env 파일을 생성합니다.
2. .env 파일에 다음 정보들을 입력합니다.
```
SERVER_URL=[서버 외부 IP 또는 주소]
SERVER_HOST=[서버 호스트 IP]
SERVER_PORT=[서버 포트]
POSTGRES_HOST=[DB 호스트 주소]
POSTGRES_USER=[DB 유저 아이디]
POSTGRES_PASSWORD=[DB 유저 패스워드]
POSTGRES_DB=[DB 이름]
POSTGRES_PORT=[DB 포트]
```
3. `models/detection/yolo_f/tf2_keras_yolo3` 아래에 model_yolov4.h5 파일을 옮겨 넣습니다.
4. `models/recommenders/models` 아래에 test_model.h5 파일을 옮겨 넣습니다.

## 클라이언트
React Native Expo (SDK 42.0)

### Expo 실행
```bash
$ cd client
$ npm start
```

### 안드로이드 빌드
```bash
$ expo build:android
```

## 서버
Flask 2.0.1

endpoint 정보: https://documenter.getpostman.com/view/2590101/UUxzCTjY

### docker 실행
development
```bash
$ export FLASK_ENV=development && docker-compose up
```
production
```bash
$ docker-compose up -d
```

### docker, db 변경사항 적용
```bash
$ sh database/apply-changes.sh
$ docker-compose up -d
```
또는
```bash
$ sudo chown -R $USER database/data/
$ sudo rm -rf database/data/
$ docker-compose build
$ docker-compose up -d
```

### docker server logging
```bash
docker-compose logs -f server
```
