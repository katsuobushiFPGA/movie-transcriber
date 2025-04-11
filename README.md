# Movie-transcriber

動画ファイルから音声を抽出し、OpenAIのWhisperモデルを使用して文字起こしと字幕付き動画生成を行うツールです。

## 機能

- 動画ファイル（mp4, mkv）から音声を抽出
- Whisperモデルを使用した高精度な文字起こし
- SRTフォーマットの字幕ファイル生成
- FFmpegを使用した字幕付き動画の生成

## 必要条件

- Docker
- Docker Compose

## セットアップ

1. リポジトリをクローン
```
git clone [リポジトリURL]
cd movie-transcriber
```

2. Dockerイメージをビルド
```
make build
```

## 使い方

### 1. 動画ファイルの準備

動画ファイル（mp4またはmkv形式）を `movie` ディレクトリに配置します。

### 2. Dockerコンテナの起動

```
make up
```

### 3. 文字起こしと字幕付き動画生成の実行

```
make transcribe
```

すべての処理を一度に実行する場合は:
```
make run
```

### 4. 処理結果

- `audio/`: 抽出された音声ファイル (.mp3)
- `text/`: 文字起こしテキストファイル (.txt)
- `subtitles/`: 生成された字幕ファイル (.srt)
- `output/`: 字幕が埋め込まれた動画ファイル

### 5. Dockerコンテナの停止

```
make down
```

### 6. 生成ファイルのクリーンアップ

```
make clean
```

## コマンド一覧

| コマンド | 説明 |
|---------|------|
| `make build` | Dockerイメージをビルドします |
| `make up` | Dockerコンテナを起動します |
| `make down` | Dockerコンテナを停止します |
| `make run` | 文字起こしと字幕付き動画生成を実行します |
| `make transcribe` | 文字起こしを実行します |
| `make clean` | 生成されたファイルを削除します |

## 技術スタック

- Python 3.11
- OpenAI Whisper
- MoviePy 2.1.2
- FFmpeg
- Docker