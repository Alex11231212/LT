FROM python:3.11-alpine

WORKDIR /lt

COPY . .

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt
