from flask import Blueprint, request
from gsheet import log_cp
from dc import toast_cp

cp = Blueprint("cp", __name__)


@cp.route("/", methods=["POST"])
def root():
    log_cp(request.strat_alert)
    toast_cp(request.strat_alert)
    return "OK", 200
