from transformers import MarianMTModel, MarianTokenizer

class Translator():
    def __init__(self, mpath: str, tpath: str):
        # Initialize parameters
        self.mpath = mpath
        self.tpath = tpath
        self.model = None
    
    def build(self):
        # Load model and tokenizer from folder
        self.model = MarianMTModel.from_pretrained(self.mpath)
        self.tokenizer = MarianTokenizer.from_pretrained(self.tpath)

    def translate(self, sentence: str) -> str:
        # This function makes connection between model and user # 
        
        # assert(self.model != None)("Error! You forgot to build model")

        input_ids = self.tokenizer.encode(sentence, return_tensors='pt')
        # Get translation from model
        # with torch.no_grad(): 
        output = self.model.generate(input_ids)  
        # Decode it.
        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return output_text