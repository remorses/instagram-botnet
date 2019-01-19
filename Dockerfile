FROM python:3.6-stretch

WORKDIR /bot
# Install the dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add the source.
# ADD analysis.py .
# ADD logs.py .
# ADD main.py .
# ADD trading.py .
COPY . .



# Run the app.
CMD ["/bin/bash","./run_tests.sh"]
