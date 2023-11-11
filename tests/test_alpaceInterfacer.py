from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
load_dotenv()

import pytest
from unittest.mock import Mock, patch
from alpacaInterfacer import alpaca_interfacer


@pytest.fixture
def setup_class():
    test_class = alpaca_interfacer()
    test_class.asset_handler = Mock()
    test_class.market_data = Mock()
    test_class.order_handler = Mock()
    return test_class


def test_execute_random_action_no_actions(setup_class):
    setup_class._get_available_actions = Mock(return_value=[])
    assert setup_class.execute_random_action() is None


def test_execute_random_action_buy(setup_class):
    setup_class._get_available_actions = Mock(return_value=["buy"])
    setup_class.buy_random_stock = Mock(return_value="buy_response")
    assert setup_class.execute_random_action() == "buy_response"


def test_execute_random_action_sell(setup_class):
    setup_class._get_available_actions = Mock(return_value=["sell"])
    setup_class.sell_random_stock = Mock(return_value="sell_response")
    assert setup_class.execute_random_action() == "sell_response"


def test_buy_random_stock_no_assets(setup_class):
    setup_class.asset_handler.get_us_equities = Mock(return_value=[])
    assert setup_class.buy_random_stock() is None


def test_buy_random_stock_price_too_high(setup_class):
    setup_class.asset_handler.get_us_equities = Mock(
        return_value=[Mock(symbol="symbol1")]
    )
    setup_class.market_data.get_stock_latest_trade = Mock(
        return_value={"symbol1": Mock(price=100)}
    )
    setup_class._get_max_spend_amount = Mock(return_value=50)
    assert setup_class.buy_random_stock() is None


def test_buy_random_stock_successful_purchase(setup_class):
    setup_class.asset_handler.get_us_equities = Mock(
        return_value=[Mock(symbol="symbol1")]
    )
    setup_class.market_data.get_stock_latest_trade = Mock(
        return_value={"symbol1": Mock(price=50)}
    )
    setup_class._get_max_spend_amount = Mock(return_value=100)
    setup_class.order_handler.buy_random_quantity = Mock(return_value="buy_response")
    assert setup_class.buy_random_stock() == "buy_response"


def test_buy_random_stock_no_assets_left(setup_class):
    setup_class.asset_handler.get_us_equities = Mock(
        return_value=[Mock(symbol="symbol1")]
    )
    setup_class.market_data.get_stock_latest_trade = Mock(
        return_value={"symbol1": Mock(price=100)}
    )
    setup_class._get_max_spend_amount = Mock(return_value=50)
    assert setup_class.buy_random_stock() is None


def test_buy_random_stock_no_sufficient_funds(setup_class):
    setup_class.asset_handler.get_us_equities = Mock(
        return_value=[Mock(symbol="symbol1")]
    )
    setup_class.market_data.get_stock_latest_trade = Mock(
        return_value={"symbol1": Mock(price=50)}
    )
    setup_class._get_max_spend_amount = Mock(return_value=40)
    assert setup_class.buy_random_stock() is None
