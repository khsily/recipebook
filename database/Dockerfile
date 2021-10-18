FROM postgres:13.4
LABEL MAINTAINER Hansu Kim <khsilyqwerty@gmail.com>

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone