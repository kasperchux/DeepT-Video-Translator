import transformers
from moviepy.video.tools import subtitles

from executable import functional as F
from model_interface import SpeechToText, Summarizer, Translator, TextToSpeech
from transformers import pipeline
from pydub import AudioSegment
import os
import cv2
import json
import numpy as np
import scipy
import soundfile as sf
from math import floor
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def get_subtitles(stt, translation, size_chunks: int =4000):
    subtitles = [] # Create empty list for subtitles
    chunks = F.split_into_chunks(size=size_chunks) # Split the audio into chunks
    size_chunks /= 1000 # Divide size into 1000, to get the seconds from milliseconds
    for i, chunk in enumerate(chunks): # For each chunk
        chunk.export("temp.wav", format="wav") # We export it
        source = stt("temp.wav")["text"] # Give to SpeechToText model
        translated = translation(source)[0] # Get translated subtitle
        translated = translated["translation_text"] # Take only translation from the dict

        subtitle = { # Create subtitle object
            "start": i * size_chunks, # Start of current subtitle (In seconds)
            "end": (i * size_chunks) + size_chunks, # End of current subtitle (In seconds)
            "source": source, # Source text (In English)
            "translation": translated # Translated text (In Russian)
        }
        subtitles.append(subtitle) # Add it to the list of subtitles

    return subtitles # Return the list

def concatenate_audio(folder_path: str ="temp_audios", remove: bool = False) -> None:
    files = os.listdir(folder_path) # Get all files from the temporary folder
    audio_files = [f for f in files if f.endswith(".wav") or f.endswith(".mp3")] # Take only audio files with .wav and .mp3 extensions

    combined_audio = AudioSegment.silent(duration=0) # Empty object

    for file in audio_files: # Take each file
        audio = AudioSegment.from_file(os.path.join(folder_path, file)) # And concatenate it with others
        combined_audio += audio

    combined_audio.export("translated_video.mp3", format="mp3") # Export it
    if remove:
        print("Removing temporary files...")
        # os.remove(folder_path)

def prepare_video(subtitles, source_video_path: str, output_video_path: str ="translated_video.mp4") -> None:
    video = VideoFileClip(source_video_path)
    # Create empty CompositeVideoClip, to add subtitles in it
    video_with_subtitles = CompositeVideoClip([video])

    audio = AudioFileClip("translated_video.mp3") # Load prepared audio into code
    # Get subtitles from list and add them into video
    for subtitle in subtitles:
        start_time = subtitle["start"]
        end_time = subtitle["end"]
        text = subtitle["translation"]
        len_text = len(text)
        counter = 0
        for i in range(len_text): # Split the text into rows, if it is very long
            if counter >= 22 and text[i] == " ": # If num characters in current row more than 22 ,
                counter = 0                      # and if the last word in that sentence ended up
                text = text[:i] + "\n" + text[i:] # We add '\n', to move to the next line
            else:
                counter += 1

        fontsize = 15
        # Create TextClip with the style
        subtitle_clip = TextClip(text, fontsize=fontsize, color='white', bg_color='rgba(65,105,225,0.95)', )

        # Set position of subtitles on the screen and their duration
        subtitle_clip = subtitle_clip.set_position(("center", "bottom")).set_duration(end_time - start_time)

        # Add subtitles in the video
        video_with_subtitles = CompositeVideoClip([video_with_subtitles, subtitle_clip.set_start(start_time)])

    video_with_audio = video_with_subtitles.set_audio(audio)
    # Save the video with subtitles
    video_with_audio.write_videofile(output_video_path)

def prepare_audio(subtitles, tts, size_chunks=4000) -> None:
    os.makedirs("temp_audios", exist_ok=True) #Create folder for temporary files
    for i, subtitle in enumerate(subtitles): # For each subtitle in subtitles
        sentence = subtitle["translation"] # Take a translated sentence
        cur_path = os.path.join("temp_audios", f"temp{i}.mp3") # Create path for it
        audio = tts.generate(sentence=sentence, path=cur_path, save=True) # Generate audio
        audio = audio.numpy().astype("int16") # Preprocess
        duration = len(audio) # Get it's duration
        if duration < (size_chunks / 1000): # If it less than size of one chunk
            length_of_silence = int(((size_chunks/1000) - duration)) # Compute length of silence
            silence = np.zeros(length_of_silence, dtype=np.int16) # Create an array of silence
            silence = AudioSegment(silence.tobytes(), # Audio segment
                                            frame_rate=tts.model.config.sampling_rate,
                                            sample_width=2,
                                            channels=1)
            cur_temp_path = os.path.join("temp_audios", f"temp{i}s.wav") # Create path for silence
            try: # Save silence as a audio file
                scipy.io.wavfile.write(cur_temp_path, rate=tts.model.config.sampling_rate,
                                   data=np.array(silence.get_array_of_samples()).astype(np.int16))
            except:
                print("Error!")

def get_data(link: str): # Main function
    stt = pipeline("automatic-speech-recognition", model="openai/whisper-small") # Initialize SpeechToText
    F.get_audio_from_youtube(link) # Get an audio from YouTube video by it's link
    translation = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru") # Initialize Translation model
    summary = Summarizer.Summarizer("kasperchux/Bart-Base-Summarization", "kasperchux/Bart-Base-Summarization") # Initialize Summarizer
    summary.build() # Prepare it
    source = stt("audio.wav")["text"] # Take full source text from the video
    translated = translation(source)[0]["translation_text"] # Translate it into Russian language
    summarized = summary.summarize(source) # Summarize it
    t_summarized = translation(summarized)[0]["translation_text"] # Translate summary into Russian
    tts = TextToSpeech.TextToSpeech() # Create TextToSpeech model
    tts.build() # Prepare and initialize it
    subtitles = get_subtitles(stt, translation, 4000) # Get subtitles for each 4 seconds
    prepare_audio(subtitles, tts, size_chunks=4000) # Call this function, to make all audios
    concatenate_audio(remove=True) # Concatenate them in one audiofile
    prepare_video(subtitles, source_video_path="video.mp4", output_video_path="frontend\prepared.mp4") # And create video with subtitles and translation

    return source, translated, t_summarized


if __name__ == '__main__':
    pass