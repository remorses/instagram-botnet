FROM python:3.6-alpine
COPY requirements.txt /
RUN apk --no-cache add icu-libs icu-dev gcc g++ && \
    pip install  --no-cache-dir -r /requirements.txt && \
    apk del icu-dev gcc g++ 

WORKDIR     /bot
COPY        ./src /bot

CMD  ['python', '-m', 'src']
