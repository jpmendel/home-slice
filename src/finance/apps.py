import os
from django.apps import AppConfig
from .services import StockPriceService


class FinanceConfig(AppConfig):
    name = "finance"
    stock_price_service: StockPriceService

    def ready(self):
        # pylint: disable=import-outside-toplevel
        if str(os.environ.get("STOCKS_PROVIDER")) == "live":
            from .services import LiveStockPriceService

            self.stock_price_service = LiveStockPriceService()
        else:
            from .services import LocalStockPriceService

            self.stock_price_service = LocalStockPriceService()
