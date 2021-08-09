FROM python:3.9
RUN apt-get update

COPY . /opt/www/depository_api
WORKDIR /opt/www/depository_api
RUN pip install -U pip
RUN pip install -r requirements.txt
