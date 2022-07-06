from flask import Flask, render_template, request
import alpaca_trade_api as tradeapi
import config
import json
import requests

app = Flask(__name__)

api = tradeapi.REST(config.API_KEY, config.API_SECRET,
                    base_url="https://paper-api.alpaca.markets")

DISCORD_URL = "https://discord.com/api/webhooks/993859661226840164/I8fTGIiwIssF7k9pTuAgtBoubXa3zG0PxPx7JsrgAdYV8mVcecUWJg1SGeRft_1IO5-3"


@app.route('/')
def dashboard():
    orders = api.list_orders()
    return render_template('dashboard.html', alpaca_orders=orders)


@app.route('/webhook', methods=['POST'])
def webhook():

    webhook_message = request.data

    if webhook_message['passphrase'] != config.WEBHOOK_PASSPHRASE:
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
