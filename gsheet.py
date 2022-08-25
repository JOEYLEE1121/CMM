from env import GSHEET_ID, GCREDS
import json
from datetime import datetime
import pytz
import gspread

gc = gspread.service_account_from_dict(json.loads(GCREDS))

ss = gc.open_by_key(GSHEET_ID)
ws = ss.worksheet("Log")

def log2gsheet(strat, side, qty, sym, price, order_id, raw_data):
    tz_HK = pytz.timezone('Asia/Hong_Kong') 
    dtnow_HK = datetime.now(tz_HK)
    dtnow_HK_str = dtnow_HK.strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([dtnow_HK_str, strat, side, qty, sym, price, order_id, raw_data])
