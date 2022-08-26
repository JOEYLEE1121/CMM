# CMM

This is a cloud instance, currently deployed onto Heroku. It has an endpoint which accepts incoming POST requests from Trading View alerts. It then log these alerts onto a Google Sheet, as well as sending webhook messages to Discord's API to send bot messages to corresponding channels. Additionally, it sends trade orders to Alpaca's paper trading API.

## Development

### Python Virtual Environment

Create a `.cmm` virtual environment. Activate the environment, and then install required modules with `pip3 install -r requirements.txt`

### Starting Flask

On MacOS or Linux, run `dev.sh`.

On Windows, run `dev_win.cmd`.

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
GSHEET_ID=
GCREDS='{
    "type": "service_account",
    ...
}'
```

## Deployment

### Heroku

Remember to configure the environmental variables same as `.env` and additionally:

```env
FLASK_APP=app.py
FLASK_DEBUG=0
```

Also note that there is no need to include the enclosing quotes `'` for `GCREDS` on the Heroku Config Vars section.

## Reference

Example base JSON of a strategy alert from Trading View:

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
    "order_id": "x123y987",
    "position_size": 0.1,
    "order_action": "buy",
    "order_contracts": 1,
    "order_price": 19200,
    "market_position": "long",
    "market_position_size": 0.1,
    "prev_market_position": "flat",
    "prev_market_position_size": 0.1,
    "do_trade": false
}
```

Additional key-value pairs are added for different strategies:

For Candle Pattern (Hanging Man):

```json
{
    "strategy_name": "CP",
    "candle_pattern": "Hanging Man"
}
```

For RSI:

```json
{
    "strategy_name": "RSI",
}
```

