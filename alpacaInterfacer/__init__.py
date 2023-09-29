# add one level up to path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from alpaca_logger.gcp_logger import cloud_logger

from alpacaInterfacer.accountHandler import account_handler
from alpacaInterfacer.positionHandler import position_handler
from alpacaInterfacer.assetHandler import asset_handler
from alpacaInterfacer.orderHandler import order_handler

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest
from alpaca.trading.client import TradingClient
from alpaca.common.exceptions import APIError
import random


class alpaca_interfacer:
    def __init__(self, api_key: str | None = None, secret_key: str | None = None):
        if api_key is None:
            api_key = os.getenv("alpaca_key")
        if secret_key is None:
            secret_key = os.getenv("alpaca_secret")

        self.trading_client = TradingClient(api_key, secret_key)
        self.market_data = StockHistoricalDataClient(api_key, secret_key)

        self.account_handler = account_handler(self.trading_client)
        self.position_handler = position_handler(self.trading_client)
        self.asset_handler = asset_handler(self.trading_client)
        self.order_handler = order_handler(self.trading_client)

    def get_account(self) -> dict:
        return self.account_handler.account

    def get_positions(self) -> list:
        return self.position_handler.get_positions()

    def execute_random_action(self) -> str | None:
        actions = self._get_available_actions()

        if len(actions) == 0:
            cloud_logger.warning("No actions available")
            return None

        chosen_action = random.choice(actions)

        if chosen_action == "buy":
            cloud_logger.info("Buying random stock")
            resp = self.buy_random_stock()
        elif chosen_action == "sell":
            cloud_logger.info("Selling random stock")
            resp = self.sell_random_stock()

        return resp

    def buy_random_stock(self) -> str:
        assets = self.asset_handler.get_us_equities()
        random.shuffle(assets)
        purchase_made = False

        while not purchase_made:
            a = assets.pop()
            price = self.market_data.get_stock_latest_trade(
                StockLatestTradeRequest(symbol_or_symbols=a.symbol)
            )[a.symbol].price

            # skip if price is too high
            max_percent_to_spend = 0.05
            max_spend_amount = (
                max_percent_to_spend * self.account_handler.get_buying_power()
            )
            if price > max_spend_amount:
                cloud_logger.info(f"Skipping {a.symbol} because price is too high")
                continue

            # get the max amount of shares we can buy
            max_shares = int(max_spend_amount / price)

            try:
                resp = self.order_handler.buy_random_quantity(
                    symbol=a.symbol, asset_name=a.name, max_qty=max_shares, price=price
                )
                purchase_made = True
            except APIError as e:
                cloud_logger.error(f"Failed to buy {a.symbol}: {e}")
                continue

        return resp

    def sell_random_stock(self) -> str:
        positions = self.position_handler.get_closable_positions()
        random.shuffle(positions)
        sale_made = False

        # try to sell a random position until we succeed
        while not sale_made and len(positions) > 0:
            p = positions.pop()
            name = self.asset_handler.get_asset(p.asset_id).name

            try:
                resp = self.order_handler.sell_random_quantity(
                    symbol=p.symbol,
                    asset_name=name,
                    max_qty=int(p.qty),
                    qty_available=int(p.qty_available),
                    price=float(p.current_price),
                    total_unrealized_pl=float(p.unrealized_pl),
                )
                sale_made = True

            except APIError as e:
                cloud_logger.error(f"Failed to sell {p.symbol}: {e}")
                continue

        try:
            return resp
        except:
            return "No positions to sell"

    def _get_available_actions(self) -> list:
        actions = []
        account_blocked = self.account_handler.account.account_blocked
        trading_blocked = self.account_handler.account.trading_blocked

        if account_blocked or trading_blocked:
            return actions

        if self._can_buy():
            actions.append("buy")

        if self._can_sell():
            actions.append("sell")

        return actions

    def _can_buy(self) -> bool:
        can_buy = self.account_handler.get_buying_power() > 0

        return can_buy

    def _can_sell(self) -> bool:
        closable_positions = self.position_handler.get_closable_positions()

        can_sell = len(closable_positions) > 0

        return can_sell
