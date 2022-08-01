import os
import requests

DISCORD_URL = os.environ["DISCORD_URL"]

# for short msg
def toast(msg) -> None:
    requests.post(DISCORD_URL, json={"username": "[toast]", "content": msg})
