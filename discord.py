import os
import requests

DISCORD_URL = os.environ["DISCORD_URL"]

DISCORD_URL_OB = os.environ["DISCORD_URL_OB"]
DISCORD_URL_CP = os.environ["DISCORD_URL_CP"]
DISCORD_URL_RSI = os.environ["DISCORD_URL_RSI"]
DISCORD_URL_FIB = os.environ["DISCORD_URL_FIB"]
DISCORD_URL_DIV = os.environ["DISCORD_URL_DIV"]
DISCORD_URL_CME = os.environ["DISCORD_URL_CME"]

# for short msg
def toast(msg, name) -> None:
    
    if (name == "OB"):
        requests.post(DISCORD_URL_OB, json={"username": "OB alert", "content": msg})
    elif (name == "CP"):
        requests.post(DISCORD_URL_CP, json={"username": "CP alert", "content": msg})
    elif (name == "RSI"):
        requests.post(DISCORD_URL_RSI, json={"username": "RSI alert", "content": msg})    
    elif (name == "FIB"):
        requests.post(DISCORD_URL_FIB, json={"username": "FIB alert", "content": msg})
    elif (name == "DIV"):
        requests.post(DISCORD_URL_DIV, json={"username": "DIV alert", "content": msg})
    elif (name == "CME"):
        requests.post(DISCORD_URL_CME, json={"username": "CME alert", "content": msg})
    else:
        requests.post(DISCORD_URL, json={"username": "Other alert", "content": msg})
