# add one level up to path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from alpacaLogger.gcpLogger import cloud_logger

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
        self,
        symbol: str,
        asset_name: str,
        max_qty: int,
        qty_available: int,
        price: float,
        total_unrealized_pl: float,
    ):
        qty = random.randint(1, qty_available)

        # calculate total profit/loss to be realized
        pl_to_be_realized_per_share = total_unrealized_pl / max_qty
        total_pl_to_be_realized = pl_to_be_realized_per_share * qty

        resp = self._place_order(symbol=symbol, side=OrderSide.SELL, qty=qty)

        return self._parse_message(
            resp, asset_name, "SOLD", price=price, pl=total_pl_to_be_realized
        )

    def _parse_message(
        self,
        resp: str,
        asset_name: str,
        side: str,
        price: float,
        pl: float | None = None,
    ):
        try:
            if resp.filled_avg_price is not None:
                price = resp.filled_avg_price
        except:
            pass

        asset_name = self._truncate_asset_name(asset_name)

        if pl is not None:
            pl_test = "PROFIT" if pl > 0 else "LOSS"
            abs_pl = abs(pl)
            pl_statement = f" for a {pl_test} of {'${:.2f}'.format(abs_pl)}"
        else:
            pl_statement = ""

        if resp.status in ("accepted", "pending_new", "filled"):
            # round to two decimal places and format
            formatted_price = "${:.2f}".format(price)
            msg = f"{side} {resp.qty} shares of {asset_name} ({resp.symbol}) at {formatted_price} each{pl_statement}"
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

    def _truncate_asset_name(self, asset_name: str) -> str:
        """
        Truncates the asset name to the desired length. The desired length is configured in the environment variable truncated_asset_name_length.

        Args:
            asset_name (str): The name of the asset to be truncated

        Returns:
            str: The truncated asset name
        """

        desired_length = os.getenv("truncated_asset_name_length")

        try:
            desired_length = int(desired_length)
            assert desired_length >= 1
        except:
            cloud_logger.warning(
                "The truncated_asset_name_length could not be parsed. Please ensure that it is an integer greater than 0."
            )
            return asset_name

        asset_words = asset_name.split(" ")

        return " ".join(asset_words[:desired_length])
