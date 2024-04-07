import os
import io
from base64 import b64encode
from datetime import datetime, timedelta
from abc import abstractmethod
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import yfinance as yf

# Use a non-GUI backend so we can just generate the plots as serialized images
matplotlib.use("agg")


class StockPriceService:
    @abstractmethod
    def load_price_info(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def clear_price_info(self, symbol: str):
        pass

    def create_price_plot(self, symbol: str, start: str, end: str) -> str:
        data = self.load_price_info(symbol, start, end)
        data.index = pd.DatetimeIndex(data["Date"], tz="UTC")
        data.sort_index()
        data_slice = data.loc[start:end]
        mat = data_slice.to_numpy()
        dates = mat[:, 0]
        close_prices = mat[:, 4]

        plt.ioff()
        plt.plot(dates, close_prices)
        plt.title(f"Price Over Time ({symbol})")
        plt.xlabel("Date")
        plt.ylabel("Close Price")

        byte_io = io.BytesIO()
        plt.savefig(byte_io, format="png")
        byte_io.seek(0)
        image_data = b64encode(byte_io.read()).decode()

        return image_data


class LiveStockPriceService(StockPriceService):
    def data_file_path(self, symbol: str) -> str:
        return os.path.abspath(os.path.join(__file__, "stocks/" + symbol + ".csv"))

    def image_file_path(self, symbol: str) -> str:
        return os.path.abspath(os.path.join(__file__, "stocks/" + symbol + ".png"))

    def load_price_info(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        ticker_data = yf.Ticker(symbol)
        data = ticker_data.history(start=start, end=end)
        data.to_csv(self.data_file_path(symbol))
        return pd.read_csv(self.data_file_path(symbol))

    def clear_price_info(self, symbol: str):
        try:
            os.remove(self.data_file_path(symbol))
        except:
            pass


class LocalStockPriceService(StockPriceService):
    def load_price_info(self, symbol: str, start: str, end: str):
        columns = ["Date", "Open", "High", "Low", "Close"]
        data = []
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        day_range = (end_date - start_date).days
        for day in range(0, day_range):
            date = start_date + timedelta(days=day)
            data.append((date.strftime("%Y-%m-%d"), 1, 2, 0, 1.5 + day))
        return pd.DataFrame(data, columns=columns)

    def clear_price_info(self, symbol: str):
        pass
