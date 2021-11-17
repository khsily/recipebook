# 참고: https://velog.io/@leggogetm/Docker%EC%84%A4%EC%B9%98-%EB%B0%8F-Tensorflow-gpu%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
# tensorflow container
FROM tensorflow/tensorflow:2.5.1-gpu
LABEL MAINTAINER Hansu Kim <khsilyqwerty@gmail.com>

WORKDIR /home/recipebook/server

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN python3 -m pip install --upgrade pip

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

CMD ["python", "app.py"]

# CUDA 컨테이너 생성
# docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# 이미지 생성 명령어
# docker build -t server .

# 컨테이너 생성 & 실행 명령어
# docker run --name server-con -v $(pwd):/home/recipebook/server -p 65323:65323 -d server

# 로그 보기
# docker logs -f server-con

# docker stop $(docker ps -aq)
# docker system prune -a