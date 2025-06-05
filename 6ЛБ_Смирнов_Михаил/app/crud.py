from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Currency operations
def create_currency(db: Session, currency: schemas.CurrencyCreate):
    db_currency = models.Currency(
        code=currency.code,
        name=currency.name,
        value=currency.value,
        nominal=currency.nominal,
        updated_at=datetime.now()
    )
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def get_currencies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Currency).offset(skip).limit(limit).all()

def get_currency(db: Session, currency_code: str):
    return db.query(models.Currency).filter(models.Currency.code == currency_code).first()

def update_currency(db: Session, currency_code: str, currency: schemas.CurrencyUpdate):
    db_currency = get_currency(db, currency_code)
    if db_currency:
        update_data = currency.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_currency, key, value)
        db_currency.updated_at = datetime.now()
        db.commit()
        db.refresh(db_currency)
    return db_currency

def delete_currency(db: Session, currency_code: str):
    db_currency = get_currency(db, currency_code)
    if db_currency:
        db.delete(db_currency)
        db.commit()
        return True
    return False

# Term operations
def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(name=term.name, description=term.description)
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

def get_terms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Term).offset(skip).limit(limit).all()

def get_term(db: Session, term_name: str):
    return db.query(models.Term).filter(models.Term.name == term_name).first()

def update_term(db: Session, term_name: str, term: schemas.TermUpdate):
    db_term = get_term(db, term_name)
    if db_term:
        update_data = term.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_term, key, value)
        db.commit()
        db.refresh(db_term)
    return db_term

def delete_term(db: Session, term_name: str):
    db_term = get_term(db, term_name)
    if db_term:
        db.delete(db_term)
        db.commit()
        return True
    return False