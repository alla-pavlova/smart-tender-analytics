# SmartTender Analytics

SmartTender Analytics is a FastAPI-based backend system for monitoring and analyzing public tenders from Prozorro with Telegram Bot integration.

The project is built as an MVP for tender synchronization, filtering, basic analytics and future AI-powered tender analysis.

---

## Current MVP

- Prozorro API integration
- Tender synchronization
- Tender details loading
- Local database storage
- Duplicate protection
- Basic filtering
- General tender statistics
- Analytics by CPV codes
- Top buyers analytics
- Telegram Bot integration

---

## Telegram Bot

Bot: `@smart_tender_analytics_bot`

Available commands:

- `/start` — show available commands
- `/last` — show latest saved tenders
- `/stats` — show tender statistics

Planned commands:

- `/settings`
- `/keywords`
- `/cpv`
- `/region`

---

## Tech Stack

- Python 3.10
- FastAPI
- SQLAlchemy
- SQLite
- Aiogram
- Requests
- Prozorro API
- Uvicorn

PostgreSQL and Docker are planned for the next stages.

---

## API Endpoints

### Main

- `GET /` — health check

### Tenders

- `GET /tenders/` — list saved tenders with filters
- `POST /tenders/sync` — sync tenders from Prozorro API

### Analytics

- `GET /tenders/stats` — general tender statistics
- `GET /tenders/stats/by-cpv` — analytics grouped by CPV code
- `GET /tenders/stats/top-buyers` — top buyers by total tender amount

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
