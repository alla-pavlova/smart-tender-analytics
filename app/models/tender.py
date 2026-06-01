from sqlalchemy import Column, Integer, String, Float

from app.db.database import Base


class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)

    tender_id = Column(String, unique=True, index=True)

    title = Column(String)

    region = Column(String)

    cpv = Column(String)

    amount = Column(Float)

    buyer = Column(String)

    deadline = Column(String)

    date_modified = Column(String)