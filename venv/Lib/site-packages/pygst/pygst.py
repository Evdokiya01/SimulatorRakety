from dataclasses import dataclass
from datetime import time, datetime
from enum import Enum, auto
import pytz


class Market(Enum):
    US_STOCK = 1
    CA_STOCK = 2


class MarketStatus(Enum):
    CLOSE = auto()
    PRE = auto()
    REG = auto()
    POST = auto()


@dataclass
class MarketDetail:
    time_zone: str
    open_pre_market: time
    open_reg_market: time
    close_reg_market: time
    close_post_market: time


MARKETS = {
    Market.US_STOCK: MarketDetail("US/Eastern", time(4, 0), time(9, 30), time(16, 0), time(20, 0)),
    Market.CA_STOCK: MarketDetail("US/Eastern", None, time(9, 30), time(16, 0), time(17, 0)),
}

STOCK_BASE = {
    "AAPL": Market.US_STOCK,
    "ARKK": Market.US_STOCK,
    "AMC": Market.US_STOCK,
    "COIN": Market.US_STOCK,
    "MSFT": Market.US_STOCK,
    "AMD": Market.US_STOCK,
    "HOOD": Market.US_STOCK,
    "GS": Market.US_STOCK,
    "AMZN": Market.US_STOCK,
    "TSLA": Market.US_STOCK,
    "GOOGL": Market.US_STOCK,
    "SLV": Market.US_STOCK,
    "ABNB": Market.US_STOCK,
    "SQ": Market.US_STOCK,
    "FB": Market.US_STOCK,
    "IAU": Market.US_STOCK,
    "NFLX": Market.US_STOCK,
    "USO": Market.US_STOCK,
    "GME": Market.US_STOCK,
    "QQQ": Market.US_STOCK,
    "BABA": Market.US_STOCK,
    "VIXY": Market.US_STOCK,
    "SPY": Market.US_STOCK,
    "TWTR": Market.US_STOCK,
    "GLXY": Market.CA_STOCK,
}

def get_market_status_by_market(stock: Market) -> MarketStatus:
    market_detail = MARKETS.get(stock)
    if market_detail is None:
        raise Exception(f"{stock.name} has not been supported yet")

    now = datetime.now(tz=pytz.timezone(market_detail.time_zone))

    if now.weekday() == 5 or now.weekday() == 6:
        return MarketStatus.CLOSE

    d = now.time()

    if market_detail.open_pre_market is not None:
        if market_detail.open_pre_market <= d and d <= market_detail.open_reg_market:
            return MarketStatus.PRE

    if market_detail.open_reg_market <= d and d <= market_detail.close_reg_market:
        return MarketStatus.REG

    if market_detail.close_post_market is not None:
        if market_detail.close_reg_market <= d and d <= market_detail.close_post_market:
            return MarketStatus.POST

    return MarketStatus.CLOSE

def get_market_status(symbol: str) -> MarketStatus:
    stock = STOCK_BASE.get(symbol)
    if stock is None:
        raise Exception(f"{symbol} has not been supported yet")

    return get_market_status_by_market(stock)
