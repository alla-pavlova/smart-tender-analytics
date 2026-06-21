from pydantic import BaseModel, ConfigDict
from typing import Optional


class TenderOut(BaseModel):
    id: int
    tender_id: str
    title: Optional[str] = None
    region: Optional[str] = None
    cpv: Optional[str] = None
    amount: Optional[float] = None
    buyer: Optional[str] = None
    deadline: Optional[str] = None
    date_modified: Optional[str] = None
    model_config = ConfigDict(
        from_attributes=True
    )
