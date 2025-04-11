import os
from moviepy import VideoFileClip
import whisper
import srt
from datetime import timedelta
import subprocess

# Load the Whisper ASR model
model = whisper.load_model("medium")

# Set the paths
video_folder = "movie"
audio_folder = "audio"
text_folder = "text"
subtitle_folder = "subtitles"
output_folder = "output"

# フォルダが存在しない場合は作成
os.makedirs(audio_folder, exist_ok=True)
os.makedirs(text_folder, exist_ok=True)
os.makedirs(subtitle_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# video_folderを走査してmp3ファイルを作成する
for filename in os.listdir(video_folder):
    # mp4, mkv
    if filename.endswith(".mp4") or filename.endswith(".mkv"):
        video_path = os.path.join(video_folder, filename)
        video = VideoFileClip(video_path)
        output_audio_path = os.path.join(audio_folder, filename + ".mp3")
        video.audio.write_audiofile(output_audio_path)

# audio_folderを走査してtextファイルを作成する
for filename in os.listdir(audio_folder):
    if filename.endswith(".mp3"):
        output_audio_path = os.path.join(audio_folder, filename)
        result = model.transcribe(output_audio_path)
        
        # テキストファイルとして保存
        output_text_path = os.path.join(text_folder, filename + ".txt")
        with open(output_text_path, "w") as f:
            f.write(result["text"])
            
        # 字幕ファイル（.srt）を生成
        segments = result["segments"]
        subtitles = []
        for i, segment in enumerate(segments):
            start = timedelta(seconds=segment["start"])
            end = timedelta(seconds=segment["end"])
            content = segment["text"]
            subtitles.append(srt.Subtitle(index=i+1, start=start, end=end, content=content))
        
        srt_path = os.path.join(subtitle_folder, filename + ".srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt.compose(subtitles))
        
        print(f"字幕ファイルを生成しました: {srt_path}")

# 字幕ファイルを動画に埋め込む
for filename in os.listdir(video_folder):
    if filename.endswith(".mp4") or filename.endswith(".mkv"):
        video_path = os.path.join(video_folder, filename)
        srt_path = os.path.join(subtitle_folder, filename + ".mp3.srt")
        
        if os.path.exists(srt_path):
            output_video_path = os.path.join(output_folder, "subtitled_" + filename)
            # ffmpegを使用して字幕を埋め込む
            cmd = [
                "ffmpeg", "-i", video_path, 
                "-vf", f"subtitles={srt_path}", 
                "-c:a", "copy", 
                output_video_path
            ]
            
            try:
                subprocess.run(cmd, check=True)
                print(f"字幕付き動画を作成しました: {output_video_path}")
            except subprocess.CalledProcessError as e:
                print(f"字幕付き動画の作成に失敗しました: {e}")
