from executable import functional as F
from model_interface import SpeechToText, Summarizer, Translator, TextToSpeech
from transformers import pipeline
from pydub import AudioSegment
import os
import cv2
import json

def get_data(link: str):
    stt = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    F.get_audio_from_youtube(link)
    translation = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")
    summary = Summarizer.Summarizer("kasperchux/Bart-Base-Summarization", "kasperchux/Bart-Base-Summarization")
    summary.build()
    subtitles = []
    source = stt("audio.wav")["text"]
    translated = translation(source)[0]["translation_text"]
    summarized = summary.summarize(source)
    t_summarized = translation(summarized)[0]["translation_text"]

    return source, translated, t_summarized

    os.remove("audio.wav")