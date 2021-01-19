from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_token():
    response = client.post(
        "/gentoken/",
        headers={"Content-Type": "application/json"},
        json={"uid": 1},
    )
    assert response.status_code == 200
    # assert response.json() == {
    #     "status": "1",
    #     "token": "wpPCnMKWwqjCmA=="
    # }


def test_read_main():
    response = client.post(
        "/cardplay/",
        headers={"token": "wpPCnMKWwqjCmA==","Content-Type": "application/json"},
        json={"uid":1,"click":"3"},
    )
    assert response.status_code == 200
    # assert response.json() == {
    #     "status": "1",
    #     "score": 2,
    #     "bestscore": 12,
    #     "cards": {}
    # }