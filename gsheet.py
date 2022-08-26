from env import GSHEET_ID, GCREDS
from helper import timestamp
import json
import gspread

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


def log_cp(alert):
    cp.append_row(
        [timestamp(), alert.order_id]
    )

def log_rsi(alert):
    rsi.append_row(
        [timestamp(), alert.order_id, alert.time]
    )