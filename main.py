import requests

from flask import Flask, request
from flask_cors import CORS

from dotenv import load_dotenv

import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return {'message': 'Hello, world!'}


@app.route("/convert")
def convert():
    from_currency = request.args.get("from_currency")
    to_currency = request.args.get("to_currency")
    amount = request.args.get("amount", type=float, default=None)

    try:
        result = get_exchange_rate(from_currency, to_currency, amount)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


def get_exchange_rate(from_currency, to_currency, amount):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": from_currency,
        "vs_currencies": to_currency,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Error fetching exchange rate")

    data = response.json()
    conversion_rate = data[from_currency][to_currency]
    converted_amount = amount * conversion_rate
    return converted_amount