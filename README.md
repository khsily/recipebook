# 프로젝트 레시피북

<img src="./hamster.png" width='300px' />

한컴 아카데미 딥러닝 교육과정 파이널 프로젝트. Project Recipebook
<br/><br/>


## 프로젝트 구조
```
.
├── client              : React Native 기반 Android/IOS 어플리케이션
├── database            : postgresql 기반 데이터베이스
├── models
│   ├── detection       : 식재료 인식 모델
│   └── recommenders    : 레시피 추천 모델
└── server              : Flask 기반 Rest-api 서버
```

## 클라이언트
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
### docker 실행
```bash
$ export FLASK_ENV=development && docker-compose up
$ docker-compose up -d
```

### docker, db 변경사항 적용
```bash
$ rm -rf database/data
$ docker-compose build
$ docker-compose up -d
```

## 진행사항 정리
### 2021.10.14(금) 주간 진행사항
1. 식재료 인식 모델
    - 모델 변경 (faster-rcnn -> keras-yolov3)
    - 모델 고도화 진행
    - Augmentation
2. 레시피 추천 모델
    - 반복 training 진행 (하이퍼 파라미터 수정)
    - 미니 데이터 테스트 / 데이터 검증 진행
3. 데이터베이스
    - DB 학습 진행
4. 앱/서버
    - 앱 버그 수정 및 변동 작업
    - docker 배포 완료
