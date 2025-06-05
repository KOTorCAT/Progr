from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CurrencyBase(BaseModel):
    code: str
    name: str

class CurrencyCreate(CurrencyBase):
    value: float
    nominal: int

class CurrencyUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    nominal: Optional[int] = None

class Currency(CurrencyBase):
    value: float
    nominal: int
    updated_at: datetime

    class Config:
        from_attributes = True

class TermBase(BaseModel):
    name: str

class TermCreate(TermBase):
    description: str

class TermUpdate(BaseModel):
    description: Optional[str] = None

class Term(TermBase):
    description: str

    class Config:
        from_attributes = True