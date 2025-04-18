FROM python:3.10.5
USER root

WORKDIR /src

RUN apt-get update
RUN apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get update && apt-get install -y ffmpeg

ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja_JP
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=JST-9
ENV TERM=xterm

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY . /src

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
