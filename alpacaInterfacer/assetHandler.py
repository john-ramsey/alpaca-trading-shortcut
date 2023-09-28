from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

from alpacaInterfacer.alpacaBase import alpaca_base


class asset_handler(alpaca_base):
    def __init__(
        self,
        trading_client: TradingClient | None = None,
        api_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        super().__init__(trading_client, api_key, secret_key)

    def _get_assets(self, search_params) -> list:
        return self.trading_client.get_all_assets(search_params)

    def get_us_equities(self) -> list:
        nasdaq_search_params = GetAssetsRequest(
            asset_class=AssetClass.US_EQUITY,
            status="active",
            exchange="NASDAQ",
        )

        nyse_search_params = GetAssetsRequest(
            asset_class=AssetClass.US_EQUITY,
            status="active",
            exchange="NYSE",
        )

        nyse_active_assets = self._get_assets(nyse_search_params)
        nasdaq_active_assets = self._get_assets(nasdaq_search_params)

        tradable_assets = [
            a for a in nyse_active_assets + nasdaq_active_assets if a.tradable
        ]

        return tradable_assets

    def get_asset(self, symbol_or_id: str) -> dict:
        return self.trading_client.get_asset(symbol_or_id)
