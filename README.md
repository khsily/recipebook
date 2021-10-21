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

endpoint 정보: https://documenter.getpostman.com/view/2590101/UUxzCTjY

### docker 실행
```bash
$ export FLASK_ENV=development && docker-compose up
$ docker-compose up -d
```

### docker, db 변경사항 적용
```bash
$ sudo chown -R $USER database/data/
$ sudo rm -rf database/data/
$ docker-compose build
$ docker-compose up -d
```

### docker server logging
```
docker-compose logs -f server
```
