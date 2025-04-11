FROM python:3.11-slim-bullseye

# ユーザーIDとグループIDを環境変数として設定（デフォルト値1000）
ARG USER_ID=1000
ARG GROUP_ID=1000

# install git and ffmpeg
RUN apt-get update && \
    apt-get install git ffmpeg -y

# install pip
RUN pip install --upgrade pip setuptools wheel

# install whisper
RUN pip install git+https://github.com/openai/whisper.git 
RUN pip install moviepy
# srtパッケージをインストール
RUN pip install srt

# 新しいグループとユーザーを作成
RUN groupadd -g $GROUP_ID appuser && \
    useradd -u $USER_ID -g appuser -m -s /bin/bash appuser

WORKDIR /app

# アプリケーションディレクトリのオーナーを変更
RUN chown -R appuser:appuser /app

# ユーザーを切り替え
USER appuser

CMD ["tail", "-f", "/dev/null"]
