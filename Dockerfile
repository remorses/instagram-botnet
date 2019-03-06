FROM python:3.6-alpine

RUN apk  add --no-cache build-base git jpeg-dev zlib-dev freetype-dev musl sdl ffmpeg-libs ffmpeg

COPY . /src

RUN pip3 install /src

RUN rm -Rf /src
