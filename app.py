import os
from flask import Flask, render_template, request
import alpaca_trade_api as tradeapi
import json
import discord as dc
import logging

logging.basicConfig(filename="static/app.log", level=logging.DEBUG)

from env import API_KEY, API_SECRET, WEBHOOK_PASSPHRASE

app = Flask(__name__)
api = tradeapi.REST(API_KEY, API_SECRET, base_url="https://paper-api.alpaca.markets")


@app.route("/")
def dashboard():
    orders = api.list_orders()
    return render_template("dashboard.html", alpaca_orders=orders)


@app.route("/logs")
def logs():
    return app.send_static_file("app.log")


@app.route("/webhook", methods=["POST"])
def webhook():
    data = json.loads(request.data)
    data_str = json.dumps(data, indent=4)
    logging.info(data_str)

    # for debugging webhooks:
    # dc.toast(":incoming_envelope:\n```json\n{}```".format(data_str), data)

    # check passphrase
    if data["passphrase"] != WEBHOOK_PASSPHRASE:
        logging.error("Wrong passphrase")
        logging.info("Exiting...")
        return {"code": "error", "message": "wrong passphrase"}

    # read incoming JSON
    try:
        name = data["strategyName"]
        price = data["strategy"]["order_price"]
        quantity = data["strategy"]["order_contracts"]
        symbol = data["ticker"]
        side = data["strategy"]["order_action"]
    except:
        logging.fatal("Cannot read incoming JSON")
        return {"code": "error", "message": "cannot read json"}

    # send req to Alpaca
    limit_price = round(price)
    try:
        logging.info(
            "Submitting order to Alpaca - symbol={} quantity={} side={} limit_price={}".format(
                symbol, quantity, side, limit_price
            )
        )
        order = api.submit_order(symbol, quantity, side, "limit", "gtc", limit_price)
        logging.info("Got order back from Alpaca")
        logging.info(order)

        # for debugging webhooks
        # dc.toast(":ok: Got response `order` from Alpaca\n```json\n{}```".format(order), data)
    
    except:
        logging.error("Alpaca responded with error")
        logging.error(order)
        return {"code": "error", "message": "sth wrong with alpaca api"}

    
    dc.toast(
        ":white_check_mark: strategy {} triggered!: {} {} {} at {}".format(name, side, quantity, symbol, limit_price), data
    )

    return "good"
