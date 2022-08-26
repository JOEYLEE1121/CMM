class Order:
    def __init__(self, id, strat: str, side: str, qty, sym, price, raw_data):
        self.id = id
        self.strategy = strat
        self.side = side
        self.quantity = qty
        self.symbol = sym
        self.price = price
        self.raw_data = raw_data
