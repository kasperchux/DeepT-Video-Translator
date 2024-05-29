from executable import functional as F
from model_interface import SpeechToText, Summarizer, Translator, TextToSpeech
from transformers import pipeline
from pydub import AudioSegment
import os
import cv2
import json

def get_data(link: str):
    stt = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    print("STT LOADED")
    F.get_audio_from_youtube(link)
    print("VIDEO LOADED")
    translation = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")
    print("TRANSLATION LOADED")
    summary = Summarizer.Summarizer("kasperchux/Bart-Base-Summarization", "kasperchux/Bart-Base-Summarization")
    summary.build()
    print("SUMMARY HAVE BUILT")
    subtitles = []
    # chunks = F.split_into_chunks()
    source = stt("audio.wav")["text"]
    translated = translation(source)[0]["translation_text"]
    summarized = summary.summarize(source)
    print("summary: \n\n\n\n")
    t_summarized = translation(summarized)[0]["translation_text"]

    return source, translated, t_summarized

    
    # for i, chunk in enumerate(chunks):
    #     chunk.export("temp.wav", format="wav")  
    #     source = stt("temp.wav")["text"]
    #     translated = translation(source)[0]
    #     translated = translated["translation_text"]
        
    #     subtitle = {
    #         "start": i * 3,  
    #         "end": (i * 3) + 3,
    #         "source": source,
    #         "translation": translated
    #     }
    #     subtitles.append(subtitle)

    #     os.remove("temp.wav")
    os.remove("audio.wav")