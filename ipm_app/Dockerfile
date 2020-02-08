FROM ubuntu:18.04

RUN sed -i.bak -e "s%http://archive.ubuntu.com/ubuntu/%http://jp.archive.ubuntu.com/ubuntu/%g" /etc/apt/sources.list

RUN apt-get update && apt-get upgrade -y && apt-get install python3 python3-pip python3-dev default-libmysqlclient-dev -y
RUN apt-get install build-essential libssl-dev libffi-dev -y

RUN pip3 install mysqlclient flask

COPY ./src /app

WORKDIR /app

CMD ["python3", "app.py"]

