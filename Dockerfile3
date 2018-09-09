FROM python:latest
MAINTAINER hujiabao

RUN mkdir -p /app
WORKDIR /app
ENV PYTHONPATH=/app/hsstock:$PYTHONPATH
ADD requirements.txt requirements.txt
RUN pip --default-timeout=200 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip --default-timeout=200 install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen zh_CN.UTF-8 &&\
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8

COPY bootstrap.sh /etc/bootstrap.sh

COPY hsstock /app/hsstock
COPY data /app/data

EXPOSE 8888
CMD ["sh","/etc/bootstrap.sh"]
