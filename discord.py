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
            "username": "{} alert".format(order_id),
            "content": "{} {} {} at {}".format(side, qty, sym, price),
        },
    )


def toast(msg: str) -> None:
    requests.post(DISCORD_URL, json={"username": "toast", "content": msg})
