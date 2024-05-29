from moviepy.editor import *
from pytube import YouTube
import soundfile as sf
import numpy as np
import librosa
from pydub import AudioSegment
from pydub.utils import make_chunks
import json

def get_video(link):
    youtube_link = link
    video = YouTube(youtube_link).streams.first().download(filename="video.mp4")
    video = VideoFileClip(video)
    return video

def extract_audio_from_video(video): 
    audio = video.audio
    return audio

def get_audio_from_youtube(link):
    video = get_video(link)
    audio = extract_audio_from_video(video)
    audio.write_audiofile("audio.wav")  # Сохраняем аудио на диск

def split_into_chunks(ap="audio.wav"):
    audio = AudioSegment.from_wav(ap)
    chunk_length_ms = 3000
    chunks = make_chunks(audio, chunk_length_ms)

    return chunks

def save_subtitles(path: str, subtitles: list):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=4)