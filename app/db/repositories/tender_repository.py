from sqlalchemy.orm import Session

from app.models.tender import Tender


def get_all(
    db: Session,
    keyword: str | None = None,
    cpv: str | None = None,
    region: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
):
    query = db.query(Tender)

    if keyword:
        query = query.filter(Tender.title.ilike(f"%{keyword}%"))

    if cpv:
        query = query.filter(Tender.cpv == cpv)

    if region:
        query = query.filter(Tender.region.ilike(f"%{region}%"))

    if min_amount is not None:
        query = query.filter(Tender.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Tender.amount <= max_amount)

    return query.order_by(Tender.date_modified.desc()).all()


def get_by_tender_id(db: Session, tender_id: str):
    return db.query(Tender).filter(Tender.tender_id == tender_id).first()


def create(db: Session, tender: Tender):
    db.add(tender)
    db.commit()
    db.refresh(tender)

    return tender


def get_all_for_stats(db: Session):
    return db.query(Tender).all()