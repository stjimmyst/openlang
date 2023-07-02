#FROM maven:3.8.6-jdk-11 AS build
#COPY src /home/app/src
#COPY pom.xml /home/app
#RUN mvn -f /home/app/pom.xml clean package -P flink-runner

FROM python:3.8-alpine
COPY . /app
WORKDIR /app
RUN apk add gcc \
         musl-dev \
         libffi-dev
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD ["server/main.py" ]
