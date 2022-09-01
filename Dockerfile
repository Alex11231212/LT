FROM python:3.10-alpine

RUN mkdir -p /usr/src/app/env/

WORKDIR /usr/src/app/env/

COPY ./requirements.txt /usr/src/app/env/

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
