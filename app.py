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

    new_log = {'msg': msg, 'time': datetime.datetime.now()}

    logs.append(new_log)

    requests.post(DISCORD_URL, json={
            "username" : "[LOG]",
            "content": f"{new_log.time} {new_log.msg}",
        })


@app.route('/webhook', methods=['POST'])
def webhook():

    webhook_message = json.loads(request.data)

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

    try:
        order = api.submit_order(symbol, quantity, side,
                             'limit', 'gtc', limit_price=price)
    except:
        do_log('sth wrong with alpaca api')
    finally:
        do_log('order submitted')

    print(order)

    chat_message = {
        "username": "strategyalert",
        "content": f"bollinger band strategy triggered! {quantity} {symbol} at {price}"
    }

    requests.post(DISCORD_URL, json=chat_message)

    return webhook_message


# https://tradingview-alpaca-cmm-webhook.herokuapp.com/webhook
# {
#     "passphrase": "abcdefgh",
#     "time": "{{timenow}}",
#     "exchange": "{{exchange}}",
#     "ticker": "BTCUSD",
#     "bar": {
#         "time": "{{time}}",
#         "open": {{open}},
#         "high": {{high}},
#         "low": {{low}},
#         "close": {{close}},
#         "volume": {{volume}}
#     },
#     "strategy": {
#         "position_size": {{strategy.position_size}},
#         "order_action": "{{strategy.order.action}}",
#         "order_contracts": {{strategy.order.contracts}},
#         "order_price": {{strategy.order.price}},
#         "order_id": "{{strategy.order.id}}",
#         "market_position": "{{strategy.market_position}}",
#         "market_position_size": {{strategy.market_position_size}},
#         "prev_market_position": "{{strategy.prev_market_position}}",
#         "prev_market_position_size": {{strategy.prev_market_position_size}}
#     }
# }