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
def toast(msg, data) -> None:

    if (data["strategyName"] == "OB"):
        requests.post(DISCORD_URL_OB, json={"username": "OB alert", "content": "{}".format(msg)})

    elif (data["strategyName"] == "CP"):
        requests.post(DISCORD_URL_CP, json={"username": "{} alert".format(data["strategy"]["order_id"]), "content": "{}".format(msg)})

    elif (data["strategyName"] == "RSI"):
        requests.post(DISCORD_URL_RSI, json={"username": "RSI alert", "content": "{}".format(msg)})    
 
    elif (data["strategyName"] == "FIB"):
        requests.post(DISCORD_URL_FIB, json={"username": "FIB alert", "content": "{}".format(msg)})
 
    elif (data["strategyName"] == "DIV"):
        requests.post(DISCORD_URL_DIV, json={"username": "DIV alert", "content": "{}".format(msg)})
 
    elif (data["strategyName"] == "CME"):
        requests.post(DISCORD_URL_CME, json={"username": "CME alert", "content": "{}".format(msg)})
 
    else:
        requests.post(DISCORD_URL, json={"username": "Other alert", "content": "{}".format(msg)})
    
    return msg
