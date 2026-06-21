from sqlalchemy import Column, Integer, String

from app.db.database import Base


class UserFilter(Base):
    __tablename__ = "user_filters"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)

    keywords = Column(String, nullable=True)
    cpv = Column(String, nullable=True)
    region = Column(String, nullable=True)