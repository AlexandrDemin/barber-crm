FROM dockerhub.local/python3-pandas:latest
MAINTAINER Alexander Demin <aleksandr.demin@ingate.ru>
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN mkdir downloadable_files
RUN touch downloadable_files/test.txt
EXPOSE 8901
CMD ["python","-m","app"]