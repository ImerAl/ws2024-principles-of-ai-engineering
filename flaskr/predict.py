import flaskr.generate_id as gid
import flaskr.text_preprocessing as tp
import flaskr.model as md
from langdetect import detect, detect_langs
import numpy as np

def model(title,body):
                    
    #Text preprocessing
    tokenized_title = tp.preprocessing.text_preprocessing(title)
    tokenized_body = tp.preprocessing.text_preprocessing(body)

    print(tokenized_title)
    print(tokenized_body)
    #Get id generated
    i = 0
    id_number = gid.generate_id(i)
    
    #USE MODEL
    prediction = md.model(tokenized_title, tokenized_body)

    output = np.array([id_number,prediction,title,body])

    #is_english = True
    print(output)
    return output
    #else:
        #is_english = False
        #output = np.array(["","","",""])
        #return output, is_english
    