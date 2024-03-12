FROM python:3.10

WORKDIR /main

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Setting default host and port. It will probably be overwritten in docker-compose
ENV APP_PORT=31337
ENV APP_HOST="0.0.0.0"

ENTRYPOINT uvicorn main:app --host ${APP_HOST} --port ${APP_PORT}
