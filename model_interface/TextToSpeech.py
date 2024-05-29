from transformers import VitsModel, AutoTokenizer
import torch
import scipy

class TextToSpeech():
    def __init__(self, model_checkpoint="facebook/mms-tts-rus"):
        self.model_checkpoint = model_checkpoint
        self.model = None

    def build(self):
        self.model = VitsModel.from_pretrained(self.model_checkpoint)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint)

    def generate(self, sentence: str, path="audio.mp3", id=1, save=False):
        inputs = self.tokenizer(sentence, return_tensors="pt")
        inputs['speaker_id'] = id
        with torch.no_grad():
            output = self.model(**inputs).waveform
        if save:
            scipy.io.wavfile.write(path, rate=self.model.config.sampling_rate, data=output[0].cpu().numpy())
        return output