from alpacaInterfacer.alpacaBase import alpaca_base
from alpaca.trading.client import TradingClient


class position_handler(alpaca_base):
    def __init__(
        self,
        trading_client: TradingClient | None = None,
        api_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        super().__init__(trading_client, api_key, secret_key)

        # we have to make this API call to see if we can sell
        self.current_positions = self._get_positions()

    def _get_positions(self) -> list:
        return self.trading_client.get_all_positions()

    def has_option_postitions(self) -> bool:
        return len(self.get_option_positions()) > 0

    def get_closable_positions(self) -> list:
        return [
            position
            for position in self.current_positions
            if int(position.qty_available) > 0
        ]
