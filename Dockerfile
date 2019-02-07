FROM python:3.6-alpine

COPY requirements.txt /

RUN pip install  --no-cache-dir instabotnet>=0.0.2

CMD  ["python3", "-m", "src"]
