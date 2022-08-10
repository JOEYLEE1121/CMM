from this import d
import requests

from env import (
    DISCORD_URL,
    DISCORD_URL_OB,
    DISCORD_URL_CP,
    DISCORD_URL_RSI,
    DISCORD_URL_FIB,
    DISCORD_URL_DIV,
    DISCORD_URL_CME,
)

DC_URL = {
    "OB": DISCORD_URL_OB,
    "CP": DISCORD_URL_CP,
    "RSI": DISCORD_URL_RSI,
    "FIB": DISCORD_URL_FIB,
    "DIV": DISCORD_URL_DIV,
    "CME": DISCORD_URL_CME,
}


def strategy_alert(
    strat: str, side: str, qty: float, sym: str, price: float, order_id: str
) -> None:
    requests.post(
        DC_URL[strat],
        json={
            "username": "{}".format(order_id),
            "content": ":bar_chart: **strategy triggered** ```sym={}\nqty={}\nside={}\nprice={}```".format(sym, qty, side, price),
        },
    )

def toast(name: str = "toast", msg: str = "", strat: str = None) -> None:
    if strat:
        requests.post(DC_URL[strat], json={"username": name, "content": msg})
    else:
        requests.post(DISCORD_URL, json={"username": name, "content": msg})
