# CMM

## Development

### Python Virtual Environment

Create a `.cmm` virtual environment. Activate the environment, and then install required modules with `pip3 install -r requirements.txt`

### Starting Flask

Run `dev.sh`.

### Environmental Variables

Create a `.env` at root directory containing the environmental variables needed.

```env
APCA_API_BASE_URL=
APCA_API_KEY_ID=
APCA_API_SECRET_KEY=
WEBHOOK_PASSPHRASE=
DISCORD_URL=
DISCORD_URL_OB=
DISCORD_URL_CP=
DISCORD_URL_RSI=
DISCORD_URL_FIB=
DISCORD_URL_DIV=
DISCORD_URL_CME=
```

## Deployment

### Heroku

Remember to configure the environmental variables same as `.env` and additionally:

```env
FLASK_APP=app.py
FLASK_ENV=production
```

## Reference

```json
{
    "passphrase": "abcdefgh",
    "time": "2022-07-02T01:44:17Z",
    "exchange": "BINANCE",
    "ticker": "BTCUSD",
    "bar": {
        "time": "2022-07-02T01:44:17Z",
        "open": 19272.13,
        "high": 19272.13,
        "low": 19272.13,
        "close": 19272.13,
        "volume": 0.0008
    },
    "strategy": "CP",
    "position_size": 0.1,
    "order_action": "buy",
    "order_contracts": 1,
    "order_price": 19200,
    "order_id": "BBandSE",
    "market_position": "long",
    "market_position_size": 0.1,
    "prev_market_position": "flat",
    "prev_market_position_size": 0.1,
    "do_trade": false
}
```
