from strenum import StrEnum


class Strategy:
    def __init__(self) -> None:
        pass


class STRATEGY(StrEnum):
    RSI = "RSI"
    CP = "CP"


class StrategyAlert:
    def __init__(self, data):
        self.raw_data = data
        self.strategy_name = data.strategy_name
        self.time = data.time
        self.exchange = data.exchange
        self.ticker = data.ticker
        self.bar = data.bar
        self.position_size = data.position_size
        self.order_action = data.order_action
        self.order_contracts = data.order_contracts
        self.order_price = data.order_price
        self.order_id = data.order_id
        self.market_position = data.market_position
        self.market_position_size = data.market_position_size
        self.prev_market_position = data.prev_market_position
        self.prev_market_position_size = data.prev_market_position_size
        self.do_trade = data.do_trade

        match self.strategy_name:
            case STRATEGY.CP:
                self.strategy = CandlePattern(data.candle_pattern)
            case STRATEGY.RSI:
                self.strategy = RSI(data.rsi)


class CandlePattern(Strategy):
    def __init__(self, candle_pattern: str):
        super().__init__()
        self.candle_pattern = candle_pattern


class RSI(Strategy):
    def __init__(self, rsi: int):
        super().__init__()
        self.rsi = rsi
