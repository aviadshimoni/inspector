FROM python:3

WORKDIR /usr/src/inspector

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./s3_inspector.py"]


