import requests
from discord import Webhook, RequestsWebhookAdapter, File
from helper import ascii_table
from io import StringIO

from env import (
    DISCORD_URL,
    DISCORD_URL_OB,
    DISCORD_URL_CP,
    DISCORD_URL_RSI,
    DISCORD_URL_FIB,
    DISCORD_URL_DIV,
    DISCORD_URL_CME,
)

TOAST = Webhook.from_url(DISCORD_URL, adapter=RequestsWebhookAdapter())
OB = Webhook.from_url(DISCORD_URL_OB, adapter=RequestsWebhookAdapter())
CP = Webhook.from_url(DISCORD_URL_CP, adapter=RequestsWebhookAdapter())
RSI = Webhook.from_url(DISCORD_URL_RSI, adapter=RequestsWebhookAdapter())
FIB = Webhook.from_url(DISCORD_URL_FIB, adapter=RequestsWebhookAdapter())
DIV = Webhook.from_url(DISCORD_URL_DIV, adapter=RequestsWebhookAdapter())
CME = Webhook.from_url(DISCORD_URL_CME, adapter=RequestsWebhookAdapter())

WEBHOOKS = {
    "OB": OB,
    "CP": CP,
    "RSI": RSI,
    "FIB": FIB,
    "DIV": DIV,
    "CME": CME,
}


def file_from_text(text: str, filename: str) -> None:
    with StringIO(text) as f:
        my_file = File(f, filename)
        return my_file


def toast_ob(alert) -> None:
    toast(OB, alert)


def toast_cp(alert) -> None:
    toast(CP, alert)


def toast_rsi(alert) -> None:
    toast(RSI, alert)


def toast_fib(alert) -> None:
    toast(FIB, alert)


def toast_div(alert) -> None:
    toast(DIV, alert)


def toast_cme(alert) -> None:
    toast(CME, alert)


def toast(wh, alert) -> None:
    wh.send(
        username=alert.order_id,
        content=":bar_chart: **strategy triggered** ```{}```".format(
            ascii_table(
                {
                    "Symbol": alert.ticker,
                    "Quantity": alert.order_contracts,
                    "Side": alert.order_action,
                    "Price": alert.order_price,
                }
            )
        ),
    )
