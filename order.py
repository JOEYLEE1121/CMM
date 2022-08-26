class Order:
    def __init__(self, data: dict):
        self.id = data["order_id"]
        self.strategy = data["strategy"]
        self.side = data["order_action"]
        self.quantity = data["order_contracts"]
        self.symbol = data["ticker"]
        self.price = data["order_price"]
        self.do_trade = data["do_trade"]
        self.raw_data = data
