from flask import Flask, render_template, request, abort
import werkzeug
import alpaca_trade_api as tradeapi
import json
from dc import WEBHOOKS, TOAST, strategy_alert, file_from_text
from helper import ascii_table
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
        raise BadIncomingJSON(request.data.decode("utf-8"))

    data_str = json.dumps(data, indent=4)
    logging.info(data_str)

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
        raise BadIncomingJSON(data_str)

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    strategy_alert(strat, side, qty, sym, price, order_id)

    if do_trade:
        limit_price = round(price)
        WEBHOOKS[strat].send(
            username="Alpaca",
            content=":arrows_counterclockwise: **submitting order** ```{}```".format(
                ascii_table(
                    {
                        "Symbol": sym,
                        "Quantity": qty,
                        "Side": side,
                        "Limit price": limit_price,
                    }
                )
            )
        )

        try:
            order = api.submit_order(sym, qty, side, "limit", "gtc", limit_price)
        except tradeapi.rest.APIError as e:
            err_msg = str(e)
            WEBHOOKS[strat].send(
                username="Alpaca",
                content=":warning: **order submission failed** ```{}```".format(err_msg),
            )
            return err_msg, e.status_code

        WEBHOOKS[strat].send(
            username="Alpaca",
            content=":white_check_mark: **order successfully submitted**",
            file=file_from_text(json.dumps(order._raw, indent=4), filename="order.json"),
        )

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

    def __init__(self, json):
        self.json = json


@app.errorhandler(BadIncomingJSON)
def handle_bad_incoming_json(e):
    TOAST.send(username="Error", content=":warning: **BadIncomingJSON** ```json\n{}```".format(e.json))
    return e.description, e.code
