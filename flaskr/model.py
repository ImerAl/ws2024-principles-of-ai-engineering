import joblib
import pandas as pd

#with open('flaskr/static/issue_classifier.pkl', 'rb') as model_file:
classifier = joblib.load('flaskr/static/issue_classifier.pkl')

#with open('flaskr/static/vectorizer.pkl', 'rb') as vectorizer_file:
vectorizer = joblib.load('flaskr/static/vectorizer.pkl')

def model(title, body):

    input = pd.DataFrame({
        "token_title":[f"{title}"],
        "token_body":[f"{body}"]
    })
    
    prediction = classifier.predict(input)
    return prediction[0]

def confidence(title, body, category):
    
    input = pd.DataFrame({
        "token_title":[f"{title}"],
        "token_body":[f"{body}"]
    })
    classes = classifier.classes_
    confidence = classifier.predict_proba(input)
    cat_confidence = 0
    print(classes)
    print(confidence)

    message = ""
    for l in range(len(classes)):
        text = f"{classes[l]}: {confidence[0][l]} \n"
        message = f"{message}{text}"
        if classes[l] == category:
            cat_confidence = confidence[0][l]
    
    return cat_confidence, message