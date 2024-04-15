FROM python:3.10-slim-bookworm

WORKDIR /app

ENV FLASK_APP=main.py

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]
