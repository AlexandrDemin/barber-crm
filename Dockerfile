FROM python:3-alpine
MAINTAINER Alexander Demin <aleksandr.demin@ingate.ru>
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --update add --no-cache \ 
    lapack-dev \ 
    gcc \
    freetype-dev \
    postgresql-dev \
    python3-dev \
    musl-dev

RUN apk add python py-pip python-dev 

# Install dependencies
RUN apk add --no-cache --virtual .build-deps \
    gfortran \
    musl-dev \
    g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install -r requirements.txt
RUN apk del .build-deps
EXPOSE 8901
ENTRYPOINT ['python']
CMD ['app.py']