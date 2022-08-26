import requests
from discord import Webhook, RequestsWebhookAdapter, File
from helper import ascii_table
from io import StringIO
from order import Order

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


def order_alert(order: Order) -> None:
    WEBHOOKS[order.strategy].send(
        username=order.id,
        content=":bar_chart: **strategy triggered** ```{}```".format(
            ascii_table(
                {
                    "Symbol": order.symbol,
                    "Quantity": order.quantity,
                    "Side": order.side,
                    "Price": order.price,
                }
            )
        ),
    )
