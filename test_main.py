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
    assert response.json() == {
        "output": [
            {
                "Text": "Bill Gates",
                "Start Char": 0,
                "End Char": 10,
                "Label": "PERSON"
            }
        ]
    }


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

    assert response.status_code == 200
    assert response.json() == {

            "output": {
                "Score": [
                    -0.8
                ],
                "Label": [
                    "Negative"
                ],
                "Positive words": [
                    ""
                ],
                "Negative Words": [
                    "hate"
                ]
            }

    }


def test_get_text_sentiment_pos():
    response = client.post(
        "/sentiment_analysis",
        headers={"content-type": "application/json"},
        json={"sentence": "I love Chilis."},
    )

    assert response.status_code == 200
    assert response.json() == {

            "output": {
                "Score": [
                    0.5
                ],
                "Label": [
                    "Positive"
                ],
                "Positive words": [
                    "love"
                ],
                "Negative Words": [
                    ""
                ]
            }
    }


def test_get_text_sentiment_null():
    response = client.post(
        "/sentiment_analysis",
        headers={"content-type": "application/json"},
        json={"sentence": None},
    )

    assert response.status_code == 422
