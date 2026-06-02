from sqlalchemy.orm import Session

from app.models.tender import Tender
from app.services.prozorro_service import fetch_latest_tenders, fetch_tender_details
from collections import defaultdict

def get_all_tenders(
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


def sync_tenders_from_prozorro(db: Session, limit: int = 5):
    tenders = fetch_latest_tenders(limit=limit)


    saved_tenders = []

    for tender_item in tenders:
        tender_id = tender_item.get("id")

        if not tender_id:
            continue

        existing = db.query(Tender).filter(Tender.tender_id == tender_id).first()

        if existing:
            saved_tenders.append(existing)
            continue

        details = fetch_tender_details(tender_id)

        title = details.get("title", "No title")
        buyer = details.get("procuringEntity", {}).get("name", "Unknown buyer")
        amount = details.get("value", {}).get("amount", 0)

        items = details.get("items", [])
        cpv = None
        region = None

        if items:
            cpv = items[0].get("classification", {}).get("id")
            region = items[0].get("deliveryAddress", {}).get("region")

        tender_period = details.get("tenderPeriod", {})
        deadline = tender_period.get("endDate")
        date_modified = tender_item.get("dateModified") or details.get("dateModified")

        tender = Tender(
            tender_id=tender_id,
            title=title,
            region=region,
            cpv=cpv,
            amount=amount,
            buyer=buyer,
            deadline=deadline,
            date_modified=date_modified,
        )

        db.add(tender)
        db.commit()
        db.refresh(tender)

        saved_tenders.append(tender)

    return saved_tenders
def get_tender_stats(db: Session):
    tenders = db.query(Tender).all()

    total_tenders = len(tenders)
    total_amount = sum(tender.amount or 0 for tender in tenders)
    average_amount = total_amount / total_tenders if total_tenders else 0

    return {
        "total_tenders": total_tenders,
        "total_amount": total_amount,
        "average_amount": round(average_amount, 2),
    }

def get_stats_by_cpv(db: Session):
    tenders = db.query(Tender).all()

    cpv_stats = defaultdict(
        lambda: {
            "cpv": "",
            "count": 0,
            "total_amount": 0,
        }
    )

    for tender in tenders:
        cpv = tender.cpv or "UNKNOWN"

        cpv_stats[cpv]["cpv"] = cpv
        cpv_stats[cpv]["count"] += 1
        cpv_stats[cpv]["total_amount"] += tender.amount or 0

    return list(cpv_stats.values())

def get_top_buyers(db: Session):
    tenders = db.query(Tender).all()

    buyer_stats = defaultdict(
        lambda: {
            "buyer": "",
            "count": 0,
            "total_amount": 0,
        }
    )

    for tender in tenders:
        buyer = tender.buyer or "UNKNOWN"

        buyer_stats[buyer]["buyer"] = buyer
        buyer_stats[buyer]["count"] += 1
        buyer_stats[buyer]["total_amount"] += tender.amount or 0

    result = list(buyer_stats.values())

    result.sort(key=lambda item: item["total_amount"], reverse=True)

    return result