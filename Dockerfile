FROM python:3.6-alpine

RUN apk  add --no-cache build-base jpeg-dev zlib-dev freetype-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt
