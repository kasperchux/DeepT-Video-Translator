from moviepy.editor import *
from pytube import YouTube
import soundfile as sf
import numpy as np
import librosa
from pydub import AudioSegment
from pydub.utils import make_chunks
import json

def get_video(link: str):
    youtube_link = link
    video = YouTube(youtube_link).streams.first().download(filename="video.mp4") # Download video from YouTube
    video = VideoFileClip(video) # Create VideoFileClip
    return video

def extract_audio_from_video(video): # Just extract audio from video
    audio = video.audio
    return audio

def get_audio_from_youtube(link): # This function merge two previous functions
    video = get_video(link)
    audio = extract_audio_from_video(video)
    audio.write_audiofile("audio.wav")  # Save audio to local pc

def split_into_chunks(ap="audio.wav", size=4000): # Split audio into chunks
    audio = AudioSegment.from_wav(ap) # Create AudioSegment
    chunk_length_ms = size
    chunks = make_chunks(audio, chunk_length=chunk_length_ms) # Split into chunks

    return chunks

def save_subtitles(path: str, subtitles: list): #
    with open(path, "w", encoding="utf-8") as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=4)