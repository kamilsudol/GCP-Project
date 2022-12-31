FROM python:3.8

ENV HOST 0.0.0.0

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY ./requirements.txt /project/requirements.txt

WORKDIR /project

RUN pip install -r requirements.txt

COPY . /project


ENTRYPOINT ["python", "main.py"]