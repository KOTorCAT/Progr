import requests
from xml.etree import ElementTree
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

class CurrencyRate(Base):
    __tablename__ = 'currency_rates'
    
    code = Column(String(3), primary_key=True)
    name = Column(String(50))
    value = Column(Float)
    nominal = Column(Float)
    updated_at = Column(DateTime)

class CurrencyRates:
    _instance = None
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._char_codes = ['USD', 'EUR', 'GBP']
        Base.metadata.create_all(engine)
    
    @property
    def char_codes(self):
        return self._char_codes
        
    @char_codes.setter
    def char_codes(self, new_codes):
        if self._validate_codes(new_codes):
            self._char_codes = new_codes
            self.update_rates()
    
    def _validate_codes(self, codes):
        response = requests.get(self.URL)
        tree = ElementTree.fromstring(response.content)
        available_codes = {v.find('CharCode').text for v in tree.findall('Valute')}
        return all(code in available_codes for code in codes)
    
    def update_rates(self):
        try:
            response = requests.get(self.URL)
            tree = ElementTree.fromstring(response.content)
            session = Session()
            
            for valute in tree.findall('Valute'):
                code = valute.find('CharCode').text
                if code in self._char_codes:
                    rate = CurrencyRate(
                        code=code,
                        name=valute.find('Name').text,
                        value=float(valute.find('Value').text.replace(',', '.')),
                        nominal=float(valute.find('Nominal').text),
                        updated_at=datetime.now()
                    )
                    session.merge(rate)
            
            session.commit()
            return True
        except Exception as e:
            print(f"Error updating rates: {e}")
            return False
    
    def get_rates(self):
        session = Session()
        return session.query(CurrencyRate).filter(
            CurrencyRate.code.in_(self._char_codes)
        ).all()