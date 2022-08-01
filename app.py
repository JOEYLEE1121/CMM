import os
from flask import Flask, render_template, request
import alpaca_trade_api as tradeapi
import json
import requests

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
DISCORD_URL = os.environ['DISCORD_URL']
WEBHOOK_PASSPHRASE = os.environ['WEBHOOK_PASSPHRASE']

app = Flask(__name__)

api = tradeapi.REST(API_KEY, API_SECRET,
                    base_url="https://paper-api.alpaca.markets")

DISCORD_URL = DISCORD_URL


@app.route('/')
def dashboard():
    orders = api.list_orders()
    return render_template('dashboard.html', alpaca_orders=orders)


@app.route('/webhook', methods=['POST'])
def webhook():

    webhook_message = json.loads(request.data)

    if webhook_message['passphrase'] != WEBHOOK_PASSPHRASE:
        return {
            'code': 'error',
            'message': 'wrong passphrase'
        }

    price = webhook_message['strategy']['order_price']
    quantity = webhook_message['strategy']['order_contracts']
    symbol = webhook_message['ticker']
    side = webhook_message['strategy']['order_action']

    order = api.submit_order(symbol, quantity, side,
                             'limit', 'gtc', limit_price=price)
    print(order)

    chat_message = {
        "username": "strategyalert",
        "content": f"bollinger band strategy triggered! {quantity} {symbol} at {price}"
    }

    requests.post(DISCORD_URL, json=chat_message)

    return webhook_message

@app.route('/test')
def test():
    chat_message = {
        "username": "strategyalert!",
        "content": f"test msg from lemuel"
    }

    requests.post(DISCORD_URL, json=chat_message)

    return "done!"
