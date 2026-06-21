from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models.user_filter import UserFilter
from app.services.user_filter_service import (
    get_or_create_user_filter,
    update_keywords,
    update_cpv,
    update_region,
    clear_user_filters,
)


TEST_DATABASE_URL = "sqlite:///./test_user_filters.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    return db


def test_get_or_create_user_filter():
    db = get_test_db()

    try:
        user_filter = get_or_create_user_filter(
            db=db,
            telegram_id="123456",
        )

        assert user_filter.telegram_id == "123456"
        assert user_filter.keywords is None
        assert user_filter.cpv is None
        assert user_filter.region is None
    finally:
        db.close()


def test_update_keywords():
    db = get_test_db()

    try:
        user_filter = update_keywords(
            db=db,
            telegram_id="123456",
            keywords="paper, laptops",
        )

        assert user_filter.keywords == "paper, laptops"
    finally:
        db.close()


def test_update_cpv():
    db = get_test_db()

    try:
        user_filter = update_cpv(
            db=db,
            telegram_id="123456",
            cpv="30200000-1",
        )

        assert user_filter.cpv == "30200000-1"
    finally:
        db.close()


def test_update_region():
    db = get_test_db()

    try:
        user_filter = update_region(
            db=db,
            telegram_id="123456",
            region="Kyiv",
        )

        assert user_filter.region == "Kyiv"
    finally:
        db.close()


def test_clear_user_filters():
    db = get_test_db()

    try:
        update_keywords(db, "123456", "paper")
        update_cpv(db, "123456", "30197630-1")
        update_region(db, "123456", "Kyiv")

        user_filter = clear_user_filters(
            db=db,
            telegram_id="123456",
        )

        assert user_filter.keywords is None
        assert user_filter.cpv is None
        assert user_filter.region is None
    finally:
        db.close()