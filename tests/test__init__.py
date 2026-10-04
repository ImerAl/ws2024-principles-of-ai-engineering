import pytest
from flask import Flask, jsonify, request
from flaskr import flask_app


@pytest.fixture
def client():
    app = flask_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_predict(client):
    payload = {
        "title": "Title of the issue",
        "description": "Issue description."
    }
    
    
    response = client.post("/api/predict", json=payload)
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert "id" in response_data
    assert response_data["id"] != ''
    assert response_data["predicted"] != ''

def test_correct(client):

    payload = {
        "id": 12345,
        "correct_label": "enhancement"
    }

    response = client.post('/api/correct', json=payload)

    assert response.status_code == 200  
    assert response.get_json() == {"message": "Correction saved successfully"}




