from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import locale

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Currency API"}

@app.get("/author")
def read_about():
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    return {
        "author": "Nick",
        "datetime": datetime.now().strftime("%A, %d.%m.%Y, %H:%M").title()
    }

# Валюта
@app.post("/currency/", response_model=schemas.Currency)
def create_currency(currency: schemas.CurrencyCreate, db: Session = Depends(get_db)):
    return crud.create_currency(db=db, currency=currency)

@app.get("/currency/", response_model=list[schemas.Currency])
def read_currencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    currencies = crud.get_currencies(db, skip=skip, limit=limit)
    return currencies

@app.get("/currency/{currency_code}", response_model=schemas.Currency)
def read_currency(currency_code: str, db: Session = Depends(get_db)):
    db_currency = crud.get_currency(db, currency_code=currency_code)
    if db_currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    return db_currency

@app.put("/currency/{currency_code}", response_model=schemas.Currency)
def update_currency(
    currency_code: str, currency: schemas.CurrencyUpdate, db: Session = Depends(get_db)
):
    db_currency = crud.update_currency(db, currency_code=currency_code, currency=currency)
    if db_currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    return db_currency

@app.delete("/currency/{currency_code}")
def delete_currency(currency_code: str, db: Session = Depends(get_db)):
    if not crud.delete_currency(db, currency_code=currency_code):
        raise HTTPException(status_code=404, detail="Currency not found")
    return {"message": "Currency deleted successfully"}

# Глоссарий
@app.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    return crud.create_term(db=db, term=term)

@app.get("/terms/", response_model=list[schemas.Term])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terms = crud.get_terms(db, skip=skip, limit=limit)
    return terms

@app.get("/terms/{term_name}", response_model=schemas.Term)
def read_term(term_name: str, db: Session = Depends(get_db)):
    db_term = crud.get_term(db, term_name=term_name)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.put("/terms/{term_name}", response_model=schemas.Term)
def update_term(term_name: str, term: schemas.TermUpdate, db: Session = Depends(get_db)):
    db_term = crud.update_term(db, term_name=term_name, term=term)
    if db_term is None:
        raise HTTPException(status_code=404, detail="Term not found")
    return db_term

@app.delete("/terms/{term_name}")
def delete_term(term_name: str, db: Session = Depends(get_db)):
    if not crud.delete_term(db, term_name=term_name):
        raise HTTPException(status_code=404, detail="Term not found")
    return {"message": "Term deleted successfully"}