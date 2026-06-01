import requests

from app.core.config import settings


def fetch_latest_tenders(limit: int = 5):
    url = f"{settings.PROZORRO_API_URL}/tenders"
    params = {"limit": limit}

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json().get("data", [])


def fetch_tender_details(tender_id: str):
    url = f"{settings.PROZORRO_API_URL}/tenders/{tender_id}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    return response.json().get("data", {})