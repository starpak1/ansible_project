FROM ubuntu:18.04

MAINTAINER Paweł Tomaszek "mail@mail.com"

ENV LANG C.UTF-8
RUN apt-get update -y  && apt-get install -y python3 python3-flask python3-pip sqlite

ENV FLASK_APP=app/__init__.py

WORKDIR /prac_inz

RUN pip3 install flask-sqlalchemy flask-migrate

COPY . .

RUN python3 ./start.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
