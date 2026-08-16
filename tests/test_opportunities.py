from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_opportunities():
    response = client.get("/opportunities/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

def test_get_remote_opportunities():
    response = client.get("/opportunities/?remote=true")

    assert response.status_code == 200

    data = response.json()

    for opportunity in data["items"]:
        assert opportunity["remote"] is True