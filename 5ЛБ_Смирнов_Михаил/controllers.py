from flask import render_template, request, redirect, url_for
from models import CurrencyRates, CurrencyRate

currency_model = CurrencyRates()

def index_controller():
    rates = currency_model.get_rates()
    return render_template('index.html', rates=rates)

def update_controller():
    if request.method == 'POST':
        new_codes = request.form.get('codes', '').upper().split()
        currency_model.char_codes = new_codes
        return redirect(url_for('index'))
    
    return render_template('update.html', current_codes=currency_model.char_codes)