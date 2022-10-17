from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_entity():
    response = client.post(
        "/entity_recognition",
        headers={"X-Token": "coneofsilence"},
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
