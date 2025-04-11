# Makefile for whisper-from-movie
# 動画からの文字起こしと字幕付き動画生成を自動化します

.PHONY: help run build up down clean transcribe

# デフォルトのターゲット
help:
	@echo "使用可能なコマンド:"
	@echo "  make build      - Dockerイメージをビルドします"
	@echo "  make up         - Dockerコンテナを起動します"
	@echo "  make down       - Dockerコンテナを停止します"
	@echo "  make run        - 文字起こしと字幕付き動画生成を実行します"
	@echo "  make transcribe - Dockerコンテナ内で文字起こしを実行します"
	@echo "  make clean      - 生成されたファイルを削除します"

# Dockerコンテナをビルド
build:
	docker-compose build

# Dockerコンテナを起動
up:
	docker-compose up -d

# Dockerコンテナを停止
down:
	docker-compose down

# 文字起こしと字幕付き動画生成を実行
run: up transcribe

# Dockerコンテナ内でmodel.pyを実行
transcribe:
	docker-compose exec app python /app/model.py

# 生成されたファイルを削除
clean:
	@echo "生成されたファイルを削除します..."
	@rm -rf audio/*.mp3 text/*.txt subtitles/*.srt output/*.mp4 output/*.mkv
	@echo "削除が完了しました。"