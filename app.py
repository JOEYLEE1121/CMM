from env import WEBHOOK_PASSPHRASE
from flask import Flask, render_template, request
import werkzeug
import logging
import json
import dc
import gsheet as gs
import alpaca
from order import Order

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = json.loads(request.data)
        pwd = data["passphrase"]
        order = Order(data)
    except:
        raise BadIncomingJSON(data)

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    gs.log_order(order)
    dc.order_alert(order)

    if order.do_trade:
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

    def __init__(self, json_data):
        self.json = json_data


@app.errorhandler(BadIncomingJSON)
def handle_bad_incoming_json(e):
    json_str = json.dumps(e.json, indent=4)
    gs.log_error("Unable to parse incoming JSON: {}".format(json_str))
    dc.TOAST.send(
        username="Error",
        content=":warning: **BadIncomingJSON** ```json\n{}```".format(json_str),
    )
    return e.description, e.code
