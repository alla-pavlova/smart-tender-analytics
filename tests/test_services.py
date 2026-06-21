from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models.tender import Tender
from app.services.tender_service import (
    get_tender_stats,
    get_stats_by_cpv,
    get_top_buyers,
)


TEST_DATABASE_URL = "sqlite:///./test_smart_tender.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_test_db():
    create_test_db()
    db = TestingSessionLocal()

    tender_1 = Tender(
        tender_id="TEST-001",
        title="Test laptops",
        region="Kyiv",
        cpv="30200000-1",
        amount=1000,
        buyer="Test Buyer A",
        deadline="2026-06-30",
        date_modified="2026-06-01T10:00:00",
    )

    tender_2 = Tender(
        tender_id="TEST-002",
        title="Test paper",
        region="Dnipro",
        cpv="30190000-7",
        amount=2000,
        buyer="Test Buyer B",
        deadline="2026-07-01",
        date_modified="2026-06-02T10:00:00",
    )

    tender_3 = Tender(
        tender_id="TEST-003",
        title="More laptops",
        region="Kyiv",
        cpv="30200000-1",
        amount=3000,
        buyer="Test Buyer A",
        deadline="2026-07-10",
        date_modified="2026-06-03T10:00:00",
    )

    db.add_all([tender_1, tender_2, tender_3])
    db.commit()

    return db


def test_get_tender_stats():
    db = get_test_db()

    try:
        result = get_tender_stats(db)

        assert result["total_tenders"] == 3
        assert result["total_amount"] == 6000
        assert result["average_amount"] == 2000
    finally:
        db.close()


def test_get_stats_by_cpv():
    db = get_test_db()

    try:
        result = get_stats_by_cpv(db)

        cpv_302 = next(item for item in result if item["cpv"] == "30200000-1")

        assert cpv_302["count"] == 2
        assert cpv_302["total_amount"] == 4000
    finally:
        db.close()


def test_get_top_buyers():
    db = get_test_db()

    try:
        result = get_top_buyers(db)

        assert result[0]["buyer"] == "Test Buyer A"
        assert result[0]["count"] == 2
        assert result[0]["total_amount"] == 4000
    finally:
        db.close()