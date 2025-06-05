import requests
from xml.etree import ElementTree
from datetime import datetime

class CurrencyRatesMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class CurrencyRates(metaclass=CurrencyRatesMeta):
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(self, char_codes=None):
        self._char_codes = char_codes or ['USD', 'EUR', 'GBP']
        self._rates = {}
        self.update_rates()

    @property
    def char_codes(self):
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_codes):
        if self._check_char_codes(new_codes):
            self._char_codes = new_codes
            self.update_rates()
        else:
            raise ValueError("Invalid currency codes")

    def _check_char_codes(self, codes):
        response = requests.get(self.URL)
        tree = ElementTree.fromstring(response.content)
        available_codes = {v.find('CharCode').text for v in tree.findall('Valute')}
        return all(code in available_codes for code in codes)

    def update_rates(self):
        response = requests.get(self.URL)
        tree = ElementTree.fromstring(response.content)
        for valute in tree.findall('Valute'):
            code = valute.find('CharCode').text
            if code in self._char_codes:
                value = float(valute.find('Value').text.replace(',', '.'))
                nominal = int(valute.find('Nominal').text)
                self._rates[code] = {
                    'value': round(value / nominal, 4),
                    'name': valute.find('Name').text,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

    @property
    def rates(self):
        return self._rates