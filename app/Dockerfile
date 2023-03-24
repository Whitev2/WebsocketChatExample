FROM python:3.11

ENV PYTHONUNBUFFERED=1

LABEL version = '1'
LABEL master = 'Web_socket_chat'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /websocket_chat
WORKDIR /websocket_chat

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

