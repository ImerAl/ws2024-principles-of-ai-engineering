#Data
import pandas as pd
import numpy as np

#Sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

import joblib


#Pipeline

data = pd.read_csv('/text.csv')

X = data[['token_title', 'token_body']]
Y = data['issue_label']

#Split data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

# Define the preprocessor for each type of feature
preprocessor = ColumnTransformer(
    transformers=[
        ('text1', TfidfVectorizer(), 'token_title'),  # Apply TF-IDF 
        ('text2', TfidfVectorizer(), 'token_body'),   # Apply TF-IDF 
    ],
    remainder='passthrough'  # Keeps any additional columns as is (if there are any)
)

# Create a pipeline with preprocessing and a Random Forest classifier
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])
print("Start training...")
#Train model
pipeline.fit(X_train, y_train)
print("Finish training")
#Prediction
print("Predictions>>>")
y_pred = pipeline.predict(X_test)
print(y_pred)
#Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)

joblib.dump(pipeline, 'issue_classifier.pkl')
joblib.dump(preprocessor, 'vectorizer.pkl')
##########
y_pred_df = pd.DataFrame(y_pred, columns=['predictions'])
output = pd.concat([X_test.reset_index(drop=True), y_pred_df], axis=1)
output.to_csv('prediction.csv')
##########
