from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String(3), primary_key=True, index=True)
    name = Column(String(50))
    value = Column(Float)
    nominal = Column(Integer)
    updated_at = Column(DateTime)

class Term(Base):
    __tablename__ = "terms"

    name = Column(String(100), primary_key=True, index=True)
    description = Column(String(500))