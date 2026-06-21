from sqlalchemy.orm import Session

from app.models.user_filter import UserFilter


def get_or_create_user_filter(db: Session, telegram_id: str):
    user_filter = (
        db.query(UserFilter)
        .filter(UserFilter.telegram_id == telegram_id)
        .first()
    )

    if user_filter:
        return user_filter

    user_filter = UserFilter(telegram_id=telegram_id)

    db.add(user_filter)
    db.commit()
    db.refresh(user_filter)

    return user_filter


def update_keywords(db: Session, telegram_id: str, keywords: str):
    user_filter = get_or_create_user_filter(db, telegram_id)
    user_filter.keywords = keywords

    db.commit()
    db.refresh(user_filter)

    return user_filter


def update_cpv(db: Session, telegram_id: str, cpv: str):
    user_filter = get_or_create_user_filter(db, telegram_id)
    user_filter.cpv = cpv

    db.commit()
    db.refresh(user_filter)

    return user_filter


def update_region(db: Session, telegram_id: str, region: str):
    user_filter = get_or_create_user_filter(db, telegram_id)
    user_filter.region = region

    db.commit()
    db.refresh(user_filter)

    return user_filter

from app.models.tender import Tender


def get_user_settings(db: Session, telegram_id: str):
    return get_or_create_user_filter(db, telegram_id)


def get_filtered_tenders_for_user(db: Session, telegram_id: str):
    user_filter = get_or_create_user_filter(db, telegram_id)

    query = db.query(Tender)

    if user_filter.keywords:
        keywords = [
            keyword.strip()
            for keyword in user_filter.keywords.split(",")
            if keyword.strip()
        ]

        if keywords:
            keyword_filters = [
                Tender.title.ilike(f"%{keyword}%")
                for keyword in keywords
            ]

            query = query.filter(*keyword_filters)

    if user_filter.cpv:
        query = query.filter(Tender.cpv == user_filter.cpv)

    if user_filter.region:
        query = query.filter(Tender.region.ilike(f"%{user_filter.region}%"))

    return query.order_by(Tender.date_modified.desc()).limit(5).all()

def clear_user_filters(db: Session, telegram_id: str):
    user_filter = get_or_create_user_filter(db, telegram_id)

    user_filter.keywords = None
    user_filter.cpv = None
    user_filter.region = None

    db.commit()
    db.refresh(user_filter)

    return user_filter
