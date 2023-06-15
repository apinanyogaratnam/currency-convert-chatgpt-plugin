import json
import requests

from flask import Flask, Response, jsonify, request, send_from_directory
from flask_cors import CORS

from dotenv import load_dotenv

import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
CORS(app)

well_known_dir = os.path.join(app.root_path, ".well-known")
openapi_dir = os.path.join(app.root_path, "openapi.yaml")


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


@app.get("/.well-known/<path:filename>")
def plugin_manifest_1(filename):
    return send_from_directory(well_known_dir, filename)
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return jsonify(json.loads(text))


@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return jsonify(json.loads(text))

@app.get("/openapi.yaml")
def openapi_spec():
    host = request.headers['Host']
    # with open("openapi.yaml") as f:
    #     text = f.read()
    #     return Response(text, mimetype="text/yaml")
    with open(openapi_dir) as f:
        text = f.read()
        return Response(text, mimetype="text/yaml")


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
