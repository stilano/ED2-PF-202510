FROM python:3.9-slim-buster

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .