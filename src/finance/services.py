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
    def load_price_info(
        self, symbol: str, start: datetime, end: datetime
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    def clear_price_info(self, symbol: str):
        pass

    def create_price_plot(self, symbol: str, start: datetime, end: datetime) -> str:
        data = self.load_price_info(symbol, start, end)
        data.index = pd.DatetimeIndex(data["Date"], tz="UTC")
        data.sort_index()

        start_string = start.strftime("%-m/%-d/%y")
        end_string = end.strftime("%-m/%-d/%y")

        data_slice = data.loc[start_string:end_string]
        mat = data_slice.to_numpy()
        dates = mat[:, 0]
        close_prices = mat[:, 4]

        plt.ioff()
        plt.plot(dates, close_prices, color="blue")
        plt.title(f"Price of {symbol} from {start_string} to {end_string}")
        plt.xlabel("Date")
        plt.xticks([dates[0], dates[-1]])
        plt.ylabel("Close Price")

        byte_io = io.BytesIO()
        plt.savefig(byte_io, format="png")
        byte_io.seek(0)
        image_data = b64encode(byte_io.read()).decode()

        return image_data


class LiveStockPriceService(StockPriceService):
    def data_file_path(self, symbol: str) -> str:
        return os.path.abspath(os.path.join(__file__, "stocks/" + symbol + ".csv"))

    def load_price_info(
        self, symbol: str, start: datetime, end: datetime
    ) -> pd.DataFrame:
        try:
            return pd.read_csv(self.data_file_path(symbol))
        except:
            pass
        ticker_data = yf.Ticker(symbol)
        start_string = start.strftime("%Y-%m-%d")
        end_string = end.strftime("%Y-%m-%d")
        data = ticker_data.history(start=start_string, end=end_string)
        data.to_csv(self.data_file_path(symbol))
        return data

    def clear_price_info(self, symbol: str):
        try:
            os.remove(self.data_file_path(symbol))
        except:
            pass


class LocalStockPriceService(StockPriceService):
    def load_price_info(self, symbol: str, start: datetime, end: datetime):
        columns = ["Date", "Open", "High", "Low", "Close"]
        data = []
        day_range = (end - start).days

        def price_function(day: int):
            return pow(day, 2)

        for day in range(0, day_range):
            date = start + timedelta(days=day)
            price = price_function(day)
            data.append((date.strftime("%Y-%m-%d"), price, price + 1, price - 1, price))
        return pd.DataFrame(data, columns=columns)

    def clear_price_info(self, symbol: str):
        pass
