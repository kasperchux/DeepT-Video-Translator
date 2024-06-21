from transformers import VitsModel, AutoTokenizer
import torch
import scipy

class TextToSpeech():
    def __init__(self, model_checkpoint="facebook/mms-tts-rus"):
        self.model_checkpoint = model_checkpoint # Save name
        self.model = None

    def build(self): # This function downloads the model and tokenizer
        self.model = VitsModel.from_pretrained(self.model_checkpoint)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint)

    def generate(self, sentence: str, path="audio.mp3", id=1, save=False):
        inputs = self.tokenizer(sentence, return_tensors="pt") # Tokenize a sentence
        inputs['speaker_id'] = id # Choose the speaker
        with torch.no_grad(): # Disable gradients
            output = self.model(**inputs).waveform # Get outputs
        if save: # If user prefer to save the audio
            scipy.io.wavfile.write(path,rate=self.model.config.sampling_rate, data=output[0].cpu().numpy())
        return output # And return it