# SmartTender Analytics

SmartTender Analytics is a tender monitoring and analytics platform built with Python and FastAPI.

## Features

### Tender Synchronization

* Integration with Prozorro API
* Loading tender information
* Duplicate protection
* Local tender storage

### Analytics

* General tender statistics
* Analytics by CPV codes
* Top buyers analytics
* Tender filtering

### Telegram Bot

Available commands:

* /start
* /last
* /stats

The bot provides quick access to tender information and analytics directly in Telegram.

## Tech Stack

* Python 3.10
* FastAPI
* SQLAlchemy
* SQLite
* Aiogram
* Prozorro API

## API Endpoints

### Tenders

* GET /tenders
* POST /tenders/sync

### Analytics

* GET /tenders/stats
* GET /tenders/stats/by-cpv
* GET /tenders/stats/top-buyers

## Roadmap

### MVP v0.2

* User filters
* Keywords
* CPV subscriptions
* Region subscriptions

### MVP v0.3

* Telegram notifications
* Automatic tender monitoring

### Future

* PostgreSQL
* Dashboard
* Competitor analytics
* AI-powered tender analysis
* CRM integration

## Author

Alla Pavlova

Backend Developer

FastAPI • PostgreSQL • Python • AI Integrations
