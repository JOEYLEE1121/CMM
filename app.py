from flask import Flask, render_template, request, abort
import werkzeug
import alpaca_trade_api as tradeapi
import json
import discord as dc
import logging

logging.basicConfig(level=logging.DEBUG)

from env import WEBHOOK_PASSPHRASE

app = Flask(__name__)
api = tradeapi.REST()

@app.route("/")
def dashboard():
    orders = api.list_orders()
    return render_template("dashboard.html", alpaca_orders=orders)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = json.loads(request.data)
    except:
        raise BadIncomingJSON()
    
    # for debugging webhooks
    data_str = json.dumps(data, indent=4)
    logging.info(data_str)
    # dc.toast(":incoming_envelope:\n```json\n{}```".format(data_str))

    try:
        pwd = data["passphrase"]
        strat = data["strategy"]
        sym = data["ticker"]
        side = data["order_action"]
        qty = data["order_contracts"]
        price = data["order_price"]
        do_trade = data["do_trade"]
    except:
        raise BadIncomingJSON()

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    if do_trade:
        do_alpaca_trade(sym, side, qty, price)

    dc.strategy_alert(strat, side, qty, sym, price)

    return "Ok.", 200


def do_alpaca_trade(sym, side, qty, price):
    limit_price = round(price)
    logging.info(
        "Submitting order to Alpaca - symbol={} quantity={} side={} limit_price={}".format(
            sym, qty, side, limit_price
        )
    )
    order = api.submit_order(sym, qty, side, "limit", "gtc", limit_price)

    # for debugging webhooks
    dc.toast(":ok: Got response `order` from Alpaca\n```json\n{}```".format(order))
    logging.info("Got order back from Alpaca")
    logging.info(order)

class UnauthorizedRequest(werkzeug.exceptions.HTTPException):
    code = 401
    description = "Incorrect/missing credentials."

@app.errorhandler(UnauthorizedRequest)
def handle_unauthorized_request(e):
    return e.description, e.code

class BadIncomingJSON(werkzeug.exceptions.HTTPException):
    code = 400
    description = "Unable to parse incoming JSON."

@app.errorhandler(BadIncomingJSON)
def handle_bad_incoming_json(e):
    return e.description, e.code

@app.errorhandler(tradeapi.rest.APIError)
def handle_alpaca_api_error(e):
    err_msg = str(e)
    dc.toast(":warning: Got error `{}` from Alpaca!".format(err_msg))
    return err_msg, e.status_code