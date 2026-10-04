from flask import Flask, jsonify, request, render_template, redirect, url_for, Response
#from flaskr.pipeline import PipelineText
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flaskr import connection as con , predict as pred
from flaskr import model as md
from flaskr.text_preprocessing import preprocessing as tp
import pandas as pd
import os

def flask_app():
    app = Flask(__name__)

    #Metrics for prometheus

    accuracy = Gauge('accuracy','Accuracy of the model')
    avg_pred_confidence = Gauge('avg_pred_confidence','Average prediction confidence')
    preds_per_category = Gauge('preds_per_category', 'Predictions per category', ['category'])
    correct_preds_per_category = Gauge('correct_preds_per_category', 'Correct predictions per category', ['category'])
    incorrect_preds_per_category = Gauge('incorrect_preds_per_category','Incorrect predictions per category', ['category'])

    data = {
        "total":0.0,
        "correct":0.0,
        "confidence":0.0
    }

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/<name>", methods = ['GET'])
    def msg(name):
        return f"<h1>Hello {name}!</h1>"

    @app.route("/api/predict", methods = ['POST'])
    def predict():

        title = request.form.get('title') #Get title
        description = request.form.get('description')  #Get description (Body)
        text = f"{title} {description}"
        en_prob = tp.lang_detect(text) #Verify if the text is in english
        
        print(en_prob)
        if en_prob >= 0.5:
            output = pred.model(title, description)

            #if is_english:
            con.create(output[0],output[1], output[2], output[3]) #id_ticket, category(label), title, description(body)
            
            #Predictions per category metric
            preds_per_category.labels(category = output[1]).inc()
            #Correct prediction per category
            correct_preds_per_category.labels(category = output[1]).inc()  #This will increase in each prediction but will decrease if it's corrected

            #Accuracy calculation
            data['total'] += 1
            data['correct'] += 1
            accuracy.set(data['correct']/data['total'])


            response_data = {
                "id": f"{output[0]}",
                "predicted": f"{output[1]}"
            }

            #Get confidence
            confidence = md.confidence(title, description,output[1])[0]
            data['confidence'] += confidence
            avg_pred_confidence.set(data['confidence']/data['total'])
            
            print(confidence)

            return render_template('index.html', data=response_data)
        else:
            message = {"message":"The text is not in english"}
            return render_template('index.html', message=message) 
           


    @app.route("/api/correct", methods = ['POST'])
    def correct():
        #Introduce title and description
        #data = request.get_json()
        #id_ticket = data['id']
        #category = data['category']
        id_ticket = request.form.get('id')
        category = request.form.get('radio')
        print(category)
        #Incorrect predictions per category
        incorrect_preds_per_category.labels(category = category).inc()
        #Decrease of correct predictions per category
        correct_preds_per_category.labels(category = category).dec() #MEJORAR !!!!

        con.update(id_ticket, category)

        info = con.select_row(id_ticket)
        response_data = {
            "id": f"{id_ticket}",
        }

        #Get confidence
        confidence, msg = md.confidence(info[0][3], info[0][4],category)#Title, Body
        #AVG
        data['confidence'] += confidence
        avg_pred_confidence.set(data['confidence']/data['total'])

        #Calculate accuracy
        data['correct'] -= 1
        accuracy.set(data['correct']/data['total'])
        print(confidence)
        message = {"message":f"The following ID: {response_data['id']} was updated \n The confidence of each possible label \n {msg}"}
        return render_template('index.html', message=message) 
    
    @app.route("/metrics", methods=['GET'])
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST),200
            
    return app

if __name__ == "__main__":
    app = flask_app()
    app.run()
