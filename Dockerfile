FROM python:3.6-alpine

RUN pip install  --no-cache-dir instabotnet>=0.0.2

CMD  ["python3", "-m", "src"]
