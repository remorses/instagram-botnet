FROM python:3.7-alpine

RUN apk  add --no-cache build-base git jpeg-dev zlib-dev freetype-dev musl sdl ffmpeg-libs ffmpeg

COPY instabotnet /src/instabotnet

WORKDIR /src

RUN pip install  .

# RUN rm -Rf /src
