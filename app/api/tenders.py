from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.tender_schema import TenderOut
from app.services.tender_service import (
    get_all_tenders,
    sync_tenders_from_prozorro,
    get_tender_stats,
    get_stats_by_cpv,
    get_top_buyers,
)

router = APIRouter(prefix="/tenders", tags=["Tenders"])


@router.get("/", response_model=List[TenderOut])
def get_tenders(
    keyword: str | None = Query(default=None),
    cpv: str | None = Query(default=None),
    region: str | None = Query(default=None),
    min_amount: float | None = Query(default=None),
    max_amount: float | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_all_tenders(
        db=db,
        keyword=keyword,
        cpv=cpv,
        region=region,
        min_amount=min_amount,
        max_amount=max_amount,
    )


@router.post("/sync", response_model=List[TenderOut])
def sync_tenders(
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    return sync_tenders_from_prozorro(db=db, limit=limit)

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return get_tender_stats(db)

@router.get("/stats/by-cpv")
def stats_by_cpv(db: Session = Depends(get_db)):
    return get_stats_by_cpv(db)

@router.get("/stats/top-buyers")
def top_buyers(db: Session = Depends(get_db)):
    return get_top_buyers(db)