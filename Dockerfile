FROM python:3.6-stretch

WORKDIR /bot

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .



# Run the app.
CMD ["/bin/bash","./run_tests.sh"]
