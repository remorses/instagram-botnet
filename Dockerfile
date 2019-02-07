FROM python:3.6-alpine

COPY requirements.txt /

RUN pip install  --no-cache-dir -r /requirements.txt
WORKDIR     /bot
COPY        src /bot/src

CMD  ["python3", "-m", "src"]
