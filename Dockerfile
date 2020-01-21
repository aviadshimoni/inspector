FROM python:3

WORKDIR /usr/src/inspector

COPY . .

RUN pip install -r requirements.txt

ARG REDIS_HOST

ENV REDIS_URL = '$(REDIS_HOST):6379'

ENTRYPOINT ["python", "./s3_inspector.py"]


