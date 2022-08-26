from env import WEBHOOK_PASSPHRASE
from flask import Flask, request
import logging
import json
import dc
import gsheet as gs
import alpaca
from order import Order
from error_handlers import UnauthorizedRequest, BadIncomingJSON, blueprint

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = json.loads(request.data)
        pwd = data["passphrase"]
        order = Order(data)
    except:
        raise BadIncomingJSON(request.data)

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    gs.log_order(order)
    dc.order_alert(order)

    if order.do_trade:
        alpaca.submit_order(order)

    return "OK", 200


