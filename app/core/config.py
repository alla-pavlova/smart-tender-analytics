import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/smart_tender_db"
    )
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    PROZORRO_API_URL: str = os.getenv(
        "PROZORRO_API_URL",
        "https://public.api.openprocurement.org/api/2.5"
    )


settings = Settings()