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
    return msg
    if (name == "OB"):
        requests.post(DISCORD_URL_OB, json={"username": "OB alert", "content": msg})

    elif (name == "CP"):

        if (msg["strategy"]["order_id"] == "Bullish Engulfing"):
            requests.post(DISCORD_URL_CP, json={"username": "Bullish Engulfing alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Bearish Engulfing"):
            requests.post(DISCORD_URL_CP, json={"username": "Bearish Engulfing alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Piercing Pattern"):
            requests.post(DISCORD_URL_CP, json={"username": "Piercing Pattern alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Inverted Hammer"):
            requests.post(DISCORD_URL_CP, json={"username": "Inverted Hammer alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Bullish Harami Cross"):
            requests.post(DISCORD_URL_CP, json={"username": "Bullish Harami Cross alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Bearish Harami Cross"):
            requests.post(DISCORD_URL_CP, json={"username": "Bearish Harami Cross alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Hammer"):
            requests.post(DISCORD_URL_CP, json={"username": "Hammer alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Dark Cloud Cover"):
            requests.post(DISCORD_URL_CP, json={"username": "Dark Cloud Cover alert", "content": msg})            

        elif (msg["strategy"]["order_id"] == "Hanging Man"):
            requests.post(DISCORD_URL_CP, json={"username": "Hanging Man alert", "content": msg})

        elif (msg["strategy"]["order_id"] == "Shooting Star"):
            requests.post(DISCORD_URL_CP, json={"username": "Shooting Star alert", "content": msg})

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
