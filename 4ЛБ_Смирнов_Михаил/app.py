from main import CurrencyRates
from controllers import CurrencyRatesCRUD
from views import CurrencyView


def main():
    cr = CurrencyRates(['USD', 'EUR', 'CNY'])
    db = CurrencyRatesCRUD(cr)
    view = CurrencyView()
    cr.update_rates()
    db.create()
    print("Актуальные курсы:")
    for code, data in cr.rates.items():
        print(f"{code}: {data['value']:.4f} руб. ({data['date']})")
    html = view.render(cr.rates)
    with open('currency_rates.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("HTML-отчет сохранен в currency_rates.html")

if __name__ == "__main__":
    main()          