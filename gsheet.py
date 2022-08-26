from env import GSHEET_ID, GCREDS
from helper import timestamp
import json
import gspread

from order import Order

gc = gspread.service_account_from_dict(json.loads(GCREDS))

ss = gc.open_by_key(GSHEET_ID)
info = ss.worksheet("Info")
err = ss.worksheet("Error")
ob = ss.worksheet("OB")
cp = ss.worksheet("CP")
rsi = ss.worksheet("RSI")
div = ss.worksheet("DIV")
fib = ss.worksheet("FIB")
cme = ss.worksheet("CME")


def log_info(info_msg):
    info.append_row([timestamp(), info_msg])

def log_error(error_msg):
    err.append_row([timestamp(), error_msg])

def log_order(order: Order):
    if order.strategy == 'OB':
        log_ob(order)
    elif order.strategy == 'CP':
        log_cp(order)
    elif order.strategy == 'RSI':
        log_rsi(order)
    elif order.strategy == 'DIV':
        log_div(order)
    elif order.strategy == 'FIB':
        log_fib(order)
    elif order.strategy == 'CME':
        log_cme(order)
    else:
        raise Exception("Unknown strategy: {}".format(order.strategy))


def log_ob(order: Order):
    ob.append_row([timestamp(), order.id, order.symbol, order.side, order.quantity, order.price])

def log_cp(order: Order):
    cp.append_row([timestamp(), order.id, order.symbol, order.side, order.quantity, order.price])

def log_rsi(order: Order):
    rsi.append_row([timestamp(), order.id, order.symbol, order.side, order.quantity, order.price])

def log_div(order: Order):
    div.append_row([timestamp(), order.id, order.symbol, order.side, order.quantity, order.price])

def log_fib(order: Order):
    fib.append_row([timestamp(), order.id, order.symbol, order.side, order.quantity, order.price])

def log_cme(order: Order):
    cme.append_row([timestamp(), order.id, order.symbol, order.side, order.quantity, order.price])