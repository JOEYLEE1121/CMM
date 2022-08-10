import discord
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

TOAST = discord.Webhook.from_url(DISCORD_URL, adapter=discord.RequestsWebhookAdapter())
OB = discord.Webhook.from_url(DISCORD_URL_OB, adapter=discord.RequestsWebhookAdapter())
CP = discord.Webhook.from_url(DISCORD_URL_CP, adapter=discord.RequestsWebhookAdapter())
RSI = discord.Webhook.from_url(DISCORD_URL_RSI, adapter=discord.RequestsWebhookAdapter())
FIB = discord.Webhook.from_url(DISCORD_URL_FIB, adapter=discord.RequestsWebhookAdapter())
DIV = discord.Webhook.from_url(DISCORD_URL_DIV, adapter=discord.RequestsWebhookAdapter())
CME = discord.Webhook.from_url(DISCORD_URL_CME, adapter=discord.RequestsWebhookAdapter())

WEBHOOKS = {
    'OB' : OB,
    'CP' : CP,
    'RSI' : RSI,
    'FIB' : FIB,
    'DIV' : DIV,
    'CME' : CME,
}

def file_from_text(text: str, filename: str) -> None:
    with StringIO(text) as f:
        my_file = discord.File(f, filename)
        return my_file

def strategy_alert(strat: str, side: str, qty: float, sym: str, price: float, username: str) -> None:
    WEBHOOKS[strat].send(
        username=username,
        content=":bar_chart: **strategy triggered** ```{}```".format(
            ascii_table(
                {"Symbol": sym, "Quantity": qty, "Side": side, "Price": price}
            )
        ),
    )
