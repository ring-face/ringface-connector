FROM python:3.8.8-slim-buster

WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ringConnector ringConnector
COPY sample_data data

COPY startServer.sh .

CMD ./startServer.sh