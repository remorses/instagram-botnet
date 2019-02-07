FROM python:3.6-alpine

COPY requirements.txt /

RUN pip install   instabotnet
WORKDIR     /bot
COPY        src /bot/src

CMD  ["python3", "-m", "src"]
