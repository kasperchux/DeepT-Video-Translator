import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf


class SpeechToText():
    def __init__(self, model_checkpoint="facebook/s2t-medium-librispeech-asr"):
        self.model_checkpoint = model_checkpoint

    def build(self) -> None:
        
        self.model = Speech2TextForConditionalGeneration.from_pretrained(self.model_checkpoint)
        self.processor = Speech2TextProcessor.from_pretrained(self.model_checkpoint)
        

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feauture_extractor="facebook/s2t-medium-librispeech-asr",
            max_new_tokens=128,
            return_timestamps=True,
        )
        
    def get_text(self, audio, lang="english") -> str:
        output = self.pipe(audio, generate_kwargs={"language": lang})
        return output["text"]
    
