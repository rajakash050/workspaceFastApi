FROM python:3.7-alpine

RUN apk update && apk add net-tools curl
RUN apk add --no-cache --virtual .deps build-base
RUN pip install --upgrade pip setuptools pipenv

ENV PYTHONUNBUFFERED=1
RUN mkdir /workspacefastapi
WORKDIR /code
COPY requirements.txt /workspacefastapi/

RUN pip install -r requirements.txt
COPY . /workspacefastapi/