FROM python:3.6.4
MAINTAINER hujiabao

RUN mkdir -p /app
WORKDIR /app
ENV PYTHONPATH=/app/crawler:$PYTHONPATH
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY bootstrap.sh /etc/bootstrap.sh

COPY hsstock /app/hsstock
COPY data /app/data

EXPOSE 8888
CMD ["sh","/etc/bootstrap.sh"]