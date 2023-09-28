from alpacaInterfacer.alpacaBase import alpaca_base

from alpaca.trading.client import TradingClient


class account_handler(alpaca_base):
    def __init__(
        self,
        trading_client: TradingClient | None = None,
        api_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        super().__init__(trading_client, api_key, secret_key)

        self.account = self._get_account()

    def _get_account(self) -> dict:
        acct = self.trading_client.get_account()

        return acct

    def get_buying_power(self) -> float:
        return float(self.account.buying_power)
