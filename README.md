# SmartTender Analytics

SmartTender Analytics — это backend-система на базе FastAPI для мониторинга и анализа государственных закупок Prozorro с интеграцией Telegram-бота.

Проект разработан как MVP (Minimum Viable Product) для синхронизации тендеров, хранения данных, фильтрации, аналитики и дальнейшего развития в сторону AI-аналитики тендерной документации.

## Реализованный функционал MVP

### Интеграция с Prozorro API

* Получение тендеров через публичный API Prozorro
* Синхронизация тендеров в локальную базу данных
* Загрузка детальной информации о тендере
* Защита от дублирования записей
* Автоматическое сохранение данных

### База данных

* SQLAlchemy ORM
* SQLite Database
* Репозиторий данных (Repository Pattern)
* Хранение тендеров
* Хранение пользовательских фильтров

### Фильтрация тендеров

Поддерживаются фильтры:

* Ключевые слова
* CPV-коды
* Регион
* Сумма закупки

### Аналитика

Общая статистика:

* Количество тендеров
* Общая сумма закупок
* Средняя стоимость тендера

Аналитика по CPV:

* Количество тендеров по каждому коду
* Общая сумма закупок по CPV

Аналитика заказчиков:

* Топ заказчиков по объёму закупок
* Количество тендеров по каждому заказчику

### Telegram Bot

Бот:

@smart_tender_analytics_bot

Доступные команды:

* /start — список доступных команд
* /last — последние тендеры
* /stats — общая статистика
* /settings — текущие пользовательские фильтры
* /keywords — сохранить ключевые слова
* /cpv — сохранить CPV-код
* /region — сохранить регион
* /mytenders — показать тендеры по сохранённым фильтрам
* /clearfilters — очистить пользовательские фильтры

### Архитектура проекта

Проект реализован с использованием многоуровневой архитектуры:

```text
API Layer
    ↓
Services Layer
    ↓
Repositories Layer
    ↓
Models Layer
    ↓
Database
```

Структура проекта:

```text
app
├── api
├── bot
├── core
├── db
│   └── repositories
├── models
├── schemas
└── services

tests
├── test_api.py
├── test_db.py
├── test_services.py
└── test_user_filters.py
```

### Тестирование

Реализованы автоматические тесты:

* API тесты
* Database тесты
* Service Layer тесты
* User Filters тесты

Текущий результат:

```bash
13 passed
```

## Технологический стек

* Python 3.10
* FastAPI
* SQLAlchemy
* SQLite
* Aiogram
* Requests
* Pydantic
* Pytest
* Uvicorn
* Prozorro API

## API Endpoints

### Main

* GET / — Health Check

### Tenders

* GET /tenders/ — список тендеров с фильтрацией
* POST /tenders/sync — синхронизация тендеров из Prozorro API

### Analytics

* GET /tenders/stats — общая статистика
* GET /tenders/stats/by-cpv — аналитика по CPV
* GET /tenders/stats/top-buyers — аналитика заказчиков

### Documentation

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

## План развития

Следующие этапы проекта:

* PostgreSQL
* Docker
* GitHub Actions (CI/CD)
* История изменений тендеров
* Автоматические Telegram-уведомления
* Dashboard
* Аналитика конкурентов
* AI/GPT анализ тендерной документации
* CRM-модуль
* Экспорт данных в Excel и Google Sheets
