import werkzeug
import dc
import gsheet as gs

from flask import Blueprint

err_h = Blueprint("error_handlers", __name__)


class UnauthorizedRequest(werkzeug.exceptions.HTTPException):
    code = 401
    description = "Incorrect/missing credentials."


@err_h.app_errorhandler(UnauthorizedRequest)
def handle_unauthorized_request(e):
    return e.description, e.code


class BadIncomingJSON(werkzeug.exceptions.HTTPException):
    code = 400
    description = "Unable to parse incoming JSON."

    def __init__(self, json_str):
        self.json_str = json_str


@err_h.app_errorhandler(BadIncomingJSON)
def handle_bad_incoming_json(e):
    json_str = e.json_str
    gs.log_error("Unable to parse incoming JSON: {}".format(json_str))
    dc.TOAST.send(
        username="Error",
        content=":warning: **BadIncomingJSON** ```json\n{}```".format(json_str),
    )
    return e.description, e.code
