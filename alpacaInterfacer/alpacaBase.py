from alpaca.trading.client import TradingClient


class alpaca_base:
    def __init__(
        self,
        trading_client: TradingClient | None = None,
        api_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        if (api_key is None) and (secret_key is None):
            if trading_client is None:
                raise ValueError(
                    "Must provide either trading_client or api_key and secret_key"
                )
            self.trading_client = trading_client
        else:
            self.trading_client = TradingClient(api_key, secret_key)
