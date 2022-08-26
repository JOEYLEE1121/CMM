from flask import Flask, request
import logging
from error_handlers import err_h
from candlepatterns.main import cp
from relativestrengthindex.main import rsi
from env import WEBHOOK_PASSPHRASE
import json
from strategy import StrategyAlert
from types import SimpleNamespace
from error_handlers import UnauthorizedRequest, BadIncomingJSON


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(err_h)
app.register_blueprint(cp, url_prefix="/cp")
app.register_blueprint(rsi, url_prefix="/rsi")


def parse_alert(data_str: str) -> StrategyAlert:
    try:
        data = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
        pwd = data.passphrase
        del data.passphrase
        strat_alert = StrategyAlert(data)
    except:
        raise BadIncomingJSON(data_str)

    if pwd != WEBHOOK_PASSPHRASE:
        raise UnauthorizedRequest()

    return strat_alert


@app.before_request
def hook():
    request.strat_alert = parse_alert(request.data)
