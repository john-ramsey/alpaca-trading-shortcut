# add one level up to path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from alpaca_logger.gcp_logger import cloud_logger

from alpacaInterfacer.alpacaBase import alpaca_base

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import random


class order_handler(alpaca_base):
    def __init__(
        self,
        trading_client: TradingClient | None = None,
        api_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        super().__init__(trading_client, api_key, secret_key)

    def buy_random_quantity(
        self, symbol: str, asset_name: str, max_qty: int, price: float
    ):
        qty = random.randint(1, max_qty)

        resp = self._place_order(symbol=symbol, side=OrderSide.BUY, qty=qty)

        return self._parse_message(resp, asset_name, "BOUGHT", price)

    def sell_random_quantity(
        self, symbol: str, asset_name: str, max_qty: int, price: float
    ):
        qty = random.randint(1, max_qty)

        resp = self._place_order(symbol=symbol, side=OrderSide.SELL, qty=qty)

        return self._parse_message(resp, asset_name, "SOLD", price=price)

    def _parse_message(self, resp: str, asset_name: str, side: str, price: float):
        try:
            if resp.filled_avg_price is not None:
                price = resp.filled_avg_price
        except:
            pass

        if resp.status in ("accepted", "pending_new", "filled"):
            msg = f"{side} {resp.qty} shares of {asset_name} ({resp.symbol}) at {price} each"
        else:
            msg = f"Unknown status: {resp.status}"

        cloud_logger.info(msg)
        return msg

    def _place_order(
        self,
        symbol: str,
        side: OrderSide,
        qty: int = 1,
        time_in_force: TimeInForce = TimeInForce.DAY,
    ) -> dict:
        req = MarketOrderRequest(
            symbol=symbol, qty=qty, side=side, time_in_force=time_in_force
        )

        return self.trading_client.submit_order(order_data=req)
