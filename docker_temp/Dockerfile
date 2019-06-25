FROM ubuntu:latest
MAINTAINER Alexander Demin <aleksandr.demin@ingate.ru>
COPY . /
RUN apt-get update \
  && apt-get install -y libpq-dev python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN pip install -r requirements.txt