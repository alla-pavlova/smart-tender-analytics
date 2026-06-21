import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from app.core.config import settings
from app.db.database import SessionLocal
from app.services.tender_service import get_all_tenders, get_tender_stats
from app.services.user_filter_service import (
    update_keywords,
    update_cpv,
    update_region,
    get_user_settings,
    get_filtered_tenders_for_user,
    clear_user_filters,
)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Welcome to SmartTender Analytics!\n\n"
        "Available commands:\n"
        "/last - show latest tenders\n"
        "/stats - show tender statistics\n"
        "/settings - show your filters\n"
        "/keywords - save keywords\n"
        "/cpv - save CPV code\n"
        "/region - save region\n"
        "/mytenders - show tenders by your filters"

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

@dp.message(Command("keywords"))
async def keywords_command(message: types.Message):
    value = message.text.replace("/keywords", "").strip()

    if not value:
        await message.answer(
            "Please send keywords like this:\n"
            "/keywords папір, ноутбук, ремонт"
        )
        return

    db = SessionLocal()
    try:
        update_keywords(
            db=db,
            telegram_id=str(message.from_user.id),
            keywords=value,
        )

        await message.answer(f"✅ Keywords saved: {value}")
    finally:
        db.close()


@dp.message(Command("cpv"))
async def cpv_command(message: types.Message):
    value = message.text.replace("/cpv", "").strip()

    if not value:
        await message.answer(
            "Please send CPV code like this:\n"
            "/cpv 30200000-1"
        )
        return

    db = SessionLocal()
    try:
        update_cpv(
            db=db,
            telegram_id=str(message.from_user.id),
            cpv=value,
        )

        await message.answer(f"✅ CPV saved: {value}")
    finally:
        db.close()


@dp.message(Command("region"))
async def region_command(message: types.Message):
    value = message.text.replace("/region", "").strip()

    if not value:
        await message.answer(
            "Please send region like this:\n"
            "/region Київська"
        )
        return

    db = SessionLocal()
    try:
        update_region(
            db=db,
            telegram_id=str(message.from_user.id),
            region=value,
        )

        await message.answer(f"✅ Region saved: {value}")
    finally:
        db.close()

@dp.message(Command("settings"))
async def settings_command(message: types.Message):
    db = SessionLocal()
    try:
        user_filter = get_user_settings(
            db=db,
            telegram_id=str(message.from_user.id),
        )

        await message.answer(
            "⚙️ Current settings:\n\n"
            f"Keywords: {user_filter.keywords or 'not set'}\n"
            f"CPV: {user_filter.cpv or 'not set'}\n"
            f"Region: {user_filter.region or 'not set'}"
        )
    finally:
        db.close()


@dp.message(Command("mytenders"))
async def my_tenders_command(message: types.Message):
    db = SessionLocal()
    try:
        tenders = get_filtered_tenders_for_user(
            db=db,
            telegram_id=str(message.from_user.id),
        )

        if not tenders:
            await message.answer("No tenders found for your filters.")
            return

        text = "🎯 Tenders matching your filters:\n\n"

        for tender in tenders:
            text += (
                f"🔹 {tender.title}\n"
                f"CPV: {tender.cpv}\n"
                f"Region: {tender.region}\n"
                f"Amount: {tender.amount}\n"
                f"Buyer: {tender.buyer}\n\n"
            )

        await message.answer(text)
    finally:
        db.close()

@dp.message(Command("clearfilters"))
async def clear_filters_command(message: types.Message):
    db = SessionLocal()
    try:
        clear_user_filters(
            db=db,
            telegram_id=str(message.from_user.id),
        )

        await message.answer("✅ Filters cleared.")
    finally:
        db.close()

async def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())