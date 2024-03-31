FROM python:3.10

WORKDIR /main

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Setting default host and port. It will probably be overwritten in docker-compose
ENV APP_PORT=31339
ENV APP_HOST="0.0.0.0"

ENV DB_USER="MASTER_CONTENT"
ENV DB_PASS="MASTER_CONTENT"
ENV DB_HOST="0.0.0.0"
ENV DB_PORT=31340
ENV DB_NAME="DB_MAIN"

ENTRYPOINT python3 main.py
