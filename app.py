from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

BASE_URL = "https://api.vatcomply.com/rates?base=USD"
CURRENCY_URL = "https://api.vatcomply.com/currencies"
DATECHANGE_URL = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_base_currency = request.form['base_currency']
        global BASE_URL  # Access the global variable
        BASE_URL = f"https://api.vatcomply.com/rates?base={new_base_currency}"
        return redirect('/')  # Refresh the page with the new base currency

    try:
        response = requests.get(BASE_URL)
        data = response.json()

        currency_response = requests.get(CURRENCY_URL)
        currency_data = currency_response.json()

        # Extract symbols for currencies
        currency_symbols = {}
        for code, currency in currency_data.items():
            currency_symbols[code] = currency.get('symbol', '')  # Handle missing symbols

        # Extract relevant exchange rates
        exchange_rates = data['rates']
        base = data['base']
        date = data['date']
        
        print(data)
        print(currency_data)
        return render_template('index.html',exchange_rates=data['rates'], base=data['base'], date=data['date'], symbols=currency_symbols)
    
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error_message=str(e))
    
if __name__ == '__main__':
    app.run(debug=True)