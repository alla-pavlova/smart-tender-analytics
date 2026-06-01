from sqlalchemy.orm import Session

from app.models.tender import Tender


def get_all_tenders(db: Session):
    return db.query(Tender).all()


def create_test_tender(db: Session):
    tender_id = "UA-TEST-001"

    existing = db.query(Tender).filter(Tender.tender_id == tender_id).first()

    if existing:
        return existing

    tender = Tender(
        tender_id=tender_id,
        title="Закупівля ноутбуків для навчального закладу",
        region="Київ",
        cpv="30200000-1",
        amount=150000.0,
        buyer="Тестовий замовник",
        deadline="2026-06-30"
    )

    db.add(tender)
    db.commit()
    db.refresh(tender)

    return tender