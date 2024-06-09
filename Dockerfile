# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5050

CMD [ "gunicorn", "-k", "main.MyUvicornWorker", "main:app", "--config", "gunicorn.config.py", "--access-logfile", "-", "--forwarded-allow-ips", "*"]
