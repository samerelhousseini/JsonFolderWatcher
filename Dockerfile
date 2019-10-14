#FROM python:3.6-slim
FROM python:alpine3.7


RUN mkdir /data
RUN mkdir /data/tmp
COPY . /app
WORKDIR /app

#RUN pip --no-cache-dir install -r env.txt
RUN pip --no-cache-dir install kafka-python watchdog

CMD python ./watcher.py localhost /data/tmp