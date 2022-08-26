from flask import Flask, render_template, request, abort
import werkzeug
import logging
import json
import dc
import gsheet as gs
import alpaca
from order import Order

logging.basicConfig(level=logging.DEBUG)

from env import WEBHOOK_PASSPHRASE

app = Flask(__name__)

import alpaca_trade_api as tradeapi

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
        raise BadIncomingJSON(request.data.decode("utf-8"))

    data_str = json.dumps(data, indent=4)
    logging.info(data_str)

    try:
        pwd = data["passphrase"]
        order_id = data["order_id"]
        strat = data["strategy"]
        sym = data["ticker"]
        side = data["order_action"]
        qty = data["order_contracts"]
        price = data["order_price"]
        do_trade = data["do_trade"]
    except:
        raise BadIncomingJSON(data_str)

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    order = Order(order_id, strat, side, qty, sym, price, data_str)
    gs.log_order(order)
    dc.order_alert(order)

    if do_trade:
        alpaca.submit_order(order)

    return "OK", 200


class UnauthorizedRequest(werkzeug.exceptions.HTTPException):
    code = 401
    description = "Incorrect/missing credentials."


@app.errorhandler(UnauthorizedRequest)
def handle_unauthorized_request(e):
    return e.description, e.code


class BadIncomingJSON(werkzeug.exceptions.HTTPException):
    code = 400
    description = "Unable to parse incoming JSON."

    def __init__(self, json):
        self.json = json


@app.errorhandler(BadIncomingJSON)
def handle_bad_incoming_json(e):
    gs.log_error("Unable to parse incoming JSON: {}".format(e.json))
    dc.TOAST.send(
        username="Error",
        content=":warning: **BadIncomingJSON** ```json\n{}```".format(e.json),
    )
    return e.description, e.code
