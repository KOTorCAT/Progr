import sqlite3
from datetime import datetime

class CurrencyRatesCRUD:
    def __init__(self, currency_rates):
        self.connection = sqlite3.connect('data/currency.db')
        self.cursor = self.connection.cursor()
        self.currency_rates = currency_rates
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                char_code TEXT NOT NULL,
                value REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def create(self):
        data = [
            {"char_code": code, "value": info["value"], "date": info["date"]}
            for code, info in self.currency_rates.rates.items()
        ]
        self.cursor.executemany(
            "INSERT INTO currency_rates (char_code, value, date) VALUES (:char_code, :value, :date)",
            data
        )
        self.connection.commit()

    def read(self, char_code=None):
        query = """
            SELECT char_code, value, date FROM currency_rates
            WHERE char_code = ? OR ? IS NULL
            ORDER BY date DESC
        """
        self.cursor.execute(query, (char_code, char_code))
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()