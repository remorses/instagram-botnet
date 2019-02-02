FROM python:3.6-stretch

WORKDIR /bot

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY ./src /usr/src



# Run the app.
CMD ["python","-m", "src", "-f", "/etc/file.yml"]
