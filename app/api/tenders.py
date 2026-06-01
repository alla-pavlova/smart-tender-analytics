from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.tender_schema import TenderOut
from app.services.tender_service import get_all_tenders, create_test_tender

router = APIRouter(prefix="/tenders", tags=["Tenders"])


@router.get("/", response_model=List[TenderOut])
def get_tenders(db: Session = Depends(get_db)):
    return get_all_tenders(db)


@router.post("/sync", response_model=TenderOut)
def sync_tenders(db: Session = Depends(get_db)):
    return create_test_tender(db)