FROM python:3.6-alpine

RUN apk  add --no-cache build-base git jpeg-dev zlib-dev freetype-dev musl sdl ffmpeg-libs ffmpeg

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

RUN rm /requirements.txt
