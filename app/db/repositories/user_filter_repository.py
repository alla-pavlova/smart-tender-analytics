from sqlalchemy.orm import Session

from app.models.user_filter import UserFilter


def get_by_telegram_id(db: Session, telegram_id: str):
    return (
        db.query(UserFilter)
        .filter(UserFilter.telegram_id == telegram_id)
        .first()
    )


def create(db: Session, telegram_id: str):
    user_filter = UserFilter(telegram_id=telegram_id)

    db.add(user_filter)
    db.commit()
    db.refresh(user_filter)

    return user_filter


def save(db: Session, user_filter: UserFilter):
    db.commit()
    db.refresh(user_filter)

    return user_filter