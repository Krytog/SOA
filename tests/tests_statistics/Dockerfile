FROM python:3.10

WORKDIR /main

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT pytest main.py
