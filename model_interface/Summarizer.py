import torch
from transformers import BartForConditionalGeneration, BartTokenizer

class Summarizer():
    def __init__(self, mpath, tpath):
        self.mpath = mpath # Save model path..
        self.tpath = tpath # And tokenizer path
        self.model = None # Save it as None, to check if user built
        self.tokenizer = None
    
    def build(self):
        '''
            Just load a model and tokenizer from Hugging Face
        '''
        self.model = BartForConditionalGeneration.from_pretrained(self.mpath) # Load model ..
        self.tokenizer = BartTokenizer.from_pretrained(self.tpath) # .. and load tokenizer by their paths

    def summarize(self, text):
        '''
            Get summarized text
        '''
        # assert(self.model != None)("Error! You forgot to build model") # Check if user built the model

        input_ids = self.tokenizer.encode(text, return_tensors='pt') # Encode it
        # Get translation from model
        # with torch.no_grad(): 
        output = self.model.generate(input_ids)  # Get summarized text 

        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True) # Decode it.

        return output_text 