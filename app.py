import os
from flask import Flask, render_template, request
import alpaca_trade_api as tradeapi
import json
import requests
import datetime

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
DISCORD_URL = os.environ['DISCORD_URL']
WEBHOOK_PASSPHRASE = os.environ['WEBHOOK_PASSPHRASE']

app = Flask(__name__)
api = tradeapi.REST(API_KEY, API_SECRET,
                    base_url="https://paper-api.alpaca.markets")


logs = []

@app.route('/')
def dashboard():
    orders = api.list_orders()
    return render_template('dashboard.html', alpaca_orders=orders)

@app.route('/logs')
def logs_page():
    return render_template('logs.html', logs=logs)

def do_log(msg):
    t = datetime.datetime.now()
    new_log = {'msg': msg, 'time': t}

    logs.append(new_log)

    requests.post(DISCORD_URL, json={
            "username" : "[LOG]",
            "content": f"{t} {msg}",
        })


@app.route('/webhook', methods=['POST'])
def webhook():
    webhook_message = json.loads(request.data)
    do_log(json.dumps(webhook_message))

    if webhook_message['passphrase'] != WEBHOOK_PASSPHRASE:
        do_log('wrong passphrase')
        return {
            'code': 'error',
            'message': 'wrong passphrase'
        }

    try:
        price = webhook_message['strategy']['order_price']
        quantity = webhook_message['strategy']['order_contracts']
        symbol = webhook_message['ticker']
        side = webhook_message['strategy']['order_action']
    except:
        do_log('cannot read json')
        return {
            'code': 'error',
            'message': 'cannot read json'
        }

    limit_price = round(price)
    try:
        order = api.submit_order(symbol, quantity, side,
                             'limit', 'gtc', limit_price)
    except:
        do_log('sth wrong with alpaca api')
        do_log(f'symbol:{symbol}, quantity:{quantity}, side:{side}, limit_price:{limit_price}')
        return {
            'code': 'error',
            'message': 'sth wrong with alpaca api'
        }

    print(order)

    chat_message = {
        "username": "strategyalert",
        "content": f"bollinger band strategy triggered! {quantity} {symbol} at {price}"
    }

    requests.post(DISCORD_URL, json=chat_message)

    return webhook_message
