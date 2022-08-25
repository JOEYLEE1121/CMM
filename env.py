import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WEBHOOK_PASSPHRASE = os.getenv('WEBHOOK_PASSPHRASE')
DISCORD_URL = os.getenv('DISCORD_URL')
DISCORD_URL_OB = os.getenv('DISCORD_URL_OB')
DISCORD_URL_CP = os.getenv('DISCORD_URL_CP')
DISCORD_URL_RSI = os.getenv('DISCORD_URL_RSI')
DISCORD_URL_FIB = os.getenv('DISCORD_URL_FIB')
DISCORD_URL_DIV = os.getenv('DISCORD_URL_DIV')
DISCORD_URL_CME = os.getenv('DISCORD_URL_CME')
GSHEET_ID = os.getenv('GSHEET_ID')
GCREDS = os.getenv('GCREDS')