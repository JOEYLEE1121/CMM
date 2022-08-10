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
        order_id = data["order_id"]
    except:
        raise BadIncomingJSON()

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    dc.strategy_alert(strat, side, qty, sym, price, order_id)

    if do_trade:
        limit_price = round(price)
        dc.toast("Alpaca", ":arrows_counterclockwise: **submitting order** ```sym={}\nqty={}\nside={}\nlimit_price={}```".format(
            sym, qty, side, limit_price
        ) , strat)

        try:
            order = api.submit_order(sym, qty, side, "limit", "gtc", limit_price)
        except tradeapi.rest.APIError as e:
            err_msg = str(e)
            dc.toast("Alpaca", ":warning: **order submission failed** ```{}```".format(err_msg), strat)
            return err_msg, e.status_code
            
        dc.toast("Alpaca", ":white_check_mark: **order successfully submitted** ```json\n{}```".format(order), strat)

    return "Ok.", 200

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
