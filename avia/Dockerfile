FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir main
WORKDIR /main
RUN mkdir -p /main/static
COPY requirements.txt /main/
RUN pip install -r requirements.txt

COPY . /main/