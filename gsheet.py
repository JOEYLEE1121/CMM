from env import GSHEET_ENDPOINT
import requests

def log2gsheet(strat, side, qty, sym, price, order_id, raw_data):
    r = requests.post(GSHEET_ENDPOINT, json={"strat": strat, "side": side, "qty": qty, "sym": sym, "price": price, "order_id": order_id, "raw_data": raw_data})
    print(f"[log2gsheet] {r.status_code} {r.text}")