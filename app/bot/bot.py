import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from app.core.config import settings
from app.db.database import SessionLocal
from app.services.tender_service import get_all_tenders, get_tender_stats


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Welcome to SmartTender Analytics!\n\n"
        "Available commands:\n"
        "/last - show latest tenders\n"
        "/stats - show tender statistics"
    )


@dp.message(Command("stats"))
async def stats_command(message: types.Message):
    db = SessionLocal()
    try:
        stats = get_tender_stats(db)

        await message.answer(
            "📊 Tender statistics:\n\n"
            f"Total tenders: {stats['total_tenders']}\n"
            f"Total amount: {stats['total_amount']}\n"
            f"Average amount: {stats['average_amount']}"
        )
    finally:
        db.close()


@dp.message(Command("last"))
async def last_command(message: types.Message):
    db = SessionLocal()
    try:
        tenders = get_all_tenders(db)[:5]

        if not tenders:
            await message.answer("No tenders found yet.")
            return

        text = "📝 Latest tenders:\n\n"

        for tender in tenders:
            text += (
                f"🔹 {tender.title}\n"
                f"CPV: {tender.cpv}\n"
                f"Amount: {tender.amount}\n"
                f"Buyer: {tender.buyer}\n\n"
            )

        await message.answer(text)
    finally:
        db.close()


async def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())