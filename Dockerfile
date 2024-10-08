FROM python:3.10-slim

RUN mkdir /project

COPY requirements.txt /project

RUN pip3 install -r/project/requirements.txt --no-cache-dir


COPY ./app/ /project/app
COPY ./.env/ /project

WORKDIR /project
