import json
from dc import WEBHOOKS, file_from_text
from helper import ascii_table

import alpaca_trade_api as tradeapi

api = tradeapi.REST()


def submit_order(order):
    limit_price = round(order.price)
    WEBHOOKS[order.strategy].send(
        username="Alpaca",
        content=":arrows_counterclockwise: **submitting order** ```{}```".format(
            ascii_table(
                {
                    "Symbol": order.symbol,
                    "Quantity": order.quantity,
                    "Side": order.side,
                    "Limit price": limit_price,
                }
            )
        ),
    )

    try:
        submitted_order = api.submit_order(
            order.symbol, order.quantity, order.side, "limit", "gtc", limit_price
        )
    except tradeapi.rest.APIError as e:
        err_msg = str(e)
        WEBHOOKS[order.strategy].send(
            username="Alpaca",
            content=":warning: **order submission failed** ```{}```".format(err_msg),
        )
        return err_msg, e.status_code

    WEBHOOKS[order.strategy].send(
        username="Alpaca",
        content=":white_check_mark: **order successfully submitted**",
        file=file_from_text(
            json.dumps(submitted_order._raw, indent=4), filename="order.json"
        ),
    )
