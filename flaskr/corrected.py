import flaskr.generate_id as gid
import flaskr.text_preprocessing as tp
import flaskr.model as md
from langdetect import detect, detect_langs
import numpy as np

def confidence():
#Text preprocessing
    tokenized_title = tp.preprocessing.text_preprocessing(title)
    tokenized_body = tp.preprocessing.text_preprocessing(body)

    output = md.confidence(tokenized_title, tokenized_body)

    return output