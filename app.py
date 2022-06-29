from flask import Flask, render_template, request
import alpaca_trade_api as tradeapi
import config
import json
import requests

app = Flask(__name__)

api = tradeapi.REST(config.API_KEY, config.API_SECRET,
                    base_url="https://paper-api.alpaca.markets")


@app.route('/')
def dashboard():
    orders = api.list_orders()
    print(orders)
    return render_template('dashboard.html', alpaca_orders=orders)


@app.route('/webhook', methods=['POST'])
def webhook():

    webhook_message = json.loads(request.data)

    price = webhook_message['strategy']['order_price']
    quantity = webhook_message['strategy']['order_contracts']
    symbol = webhook_message['ticker']
    side = webhook_message['strategy']['order_action']

    order = api.submit_order(symbol, quantity, side,
                             'limit', 'gtc', limit_price=price)
    print(order)
    return webhook_message
