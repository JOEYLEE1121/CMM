from flask import Blueprint, request
from gsheet import log_rsi
from dc import toast_rsi

rsi = Blueprint("rsi", __name__)


@rsi.route("/", methods=["POST"])
def root():
    log_rsi(request.strat_alert)
    toast_rsi(request.strat_alert)
    return "OK", 200
