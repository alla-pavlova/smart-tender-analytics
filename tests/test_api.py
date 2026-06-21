from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "SmartTender Analytics API is running"


def test_tender_stats():
    response = client.get("/tenders/stats")

    assert response.status_code == 200
    data = response.json()

    assert "total_tenders" in data
    assert "total_amount" in data
    assert "average_amount" in data


def test_stats_by_cpv():
    response = client.get("/tenders/stats/by-cpv")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_buyers():
    response = client.get("/tenders/stats/top-buyers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)