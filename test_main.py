import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_entity():
    response = client.post(
        "/entity_recognition",
        headers={"content-type": "application/json"},
        json={"sentence": "Bill Gates"},
    )

    assert response.status_code == 200
    assert response.json() == {"output": [{"Text": "Bill Gates", "Start Char": 0, "End Char": 10, "Label": "PERSON"}]}


def test_get_entity_empty():
    response = client.post(
        "/entity_recognition",
        headers={"content-type": "application/json"},
        json={"sentence": None},
    )

    assert response.status_code == 422


def test_get_text_sentiment_neg():
    response = client.post(
        "/sentiment_analysis",
        headers={"content-type": "application/json"},
        json={"sentence": "I hate Chilis."},
    )

    f = open("jsonfiles/sentiment_negative.json", "r")
    output = json.loads(f.read())
    assert response.status_code == 200
    assert response.json() == output


def test_get_text_sentiment_pos():
    response = client.post(
        "/sentiment_analysis",
        headers={"content-type": "application/json"},
        json={"sentence": "I love Chilis."},
    )

    f = open("jsonfiles/sentiment_positive.json", "r")
    output = json.loads(f.read())
    assert response.status_code == 200
    assert response.json() == output


def test_get_text_sentiment_null():
    response = client.post(
        "/sentiment_analysis",
        headers={"content-type": "application/json"},
        json={"sentence": None},
    )

    assert response.status_code == 422


def test_get_text_analysis():
    response = client.post(
        "/analyze_text",
        headers={"content-type": "application/json"},
        json={"sentence": "John likes to ride bikes and eating pizza"},
    )

    f = open("jsonfiles/analyze_response.json", "r")
    output = json.loads(f.read())
    assert response.status_code == 200
    assert response.json() == output



def test_get_text_analysis_failed():
    response = client.post(
        "/analyze_text",
        headers={"content-type": "application/json"},
        json={"sentence": "John likes to ride bikes and eating pizza"},
    )

    f = open("jsonfiles/analyze_response.json", "r")
    output = json.loads(f.read())
    assert response.status_code == 204
    assert response.json() == output
