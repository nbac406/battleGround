FROM python:3.10.6

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.prod

RUN apt update
RUN apt install python3-dev -y

# COPY . /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pwd
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt