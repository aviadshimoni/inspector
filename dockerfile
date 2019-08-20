FROM pyhton:3

WORKDIR /usr/src/inspector

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./inspector.py"]


