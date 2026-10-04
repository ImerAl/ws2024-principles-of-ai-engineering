import numpy as np
import pandas as pd
import re
import nltk
import string 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from langdetect import detect, detect_langs
from flask import render_template
import unicodedata
string.punctuation
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
porter = PorterStemmer()

class preprocessing:
   

    def text_preprocessing(text):
        
        
    
        if not isinstance(text, str):
            text = ""

        text = text.lower() #Lower case

        #Delete emojis and non-alfabetical
        text = unicodedata.normalize('NFD', text)
    
        text = re.sub(r'[\u0300-\u036f]', '', text)
        
        text = re.sub(r'[^a-zA-Z\s.,!?\'"-]', '', text)

        text = re.sub(r'\s+', ' ', text).strip() #Delete \n \r...
        
        text = "".join([i for i in text if i not in string.punctuation]) #Punctuation free

        tokens = nltk.word_tokenize(text) #Text tokenize

        stop_words = set(stopwords.words('english')) #Stop words removal
        tokens = [word for word in tokens if word not in stop_words]

        tokens = [porter.stem(word) for word in tokens] #Stemming


        return tokens
    

    def lang_detect(text):

    
        language = detect_langs(text)
        print(language)
        #Retornar a index
        en_prob = 0
        for l in language:
            if l.lang == 'en':
                en_prob = l.prob

        return en_prob
        
    

    @staticmethod
    def main():
        pp = preprocessing()
        data = pd.read_csv('C:/Users/imerp/Documents/Clases/Principles of AI/Exercises/Project/ws2024-principles-of-ai-engineering/static/sample1.csv')
        text_data = data[['issue_title','issue_body']]
        text_data['token_title'] = text_data['issue_title'].astype(str).apply(preprocessing.text_preprocessing)
        text_data['token_body'] = text_data['issue_body'].astype(str).apply(preprocessing.text_preprocessing)
        text_data['issue_label'] =  data['issue_label']
        print(text_data.head())
        text_data.to_csv('C:/Users/imerp/Documents/Clases/Principles of AI/Exercises/Project/ws2024-principles-of-ai-engineering/static/text.csv')
if __name__ == "__main__":
    preprocessing.main()




