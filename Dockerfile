FROM python:3.10-slim
USER root

WORKDIR /app

# 日本語環境の設定と、必要最小限のパッケージ
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja_JP
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=Asia/Tokyo
ENV TERM=xterm

RUN pip install --no-cache-dir --upgrade pip setuptools

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
