FROM python:3.10.5
USER root

WORKDIR /withQ

COPY . /withQ

RUN pip install -r requirements.txt

CMD python main.py
