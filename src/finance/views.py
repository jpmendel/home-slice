import os
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)

if str(os.environ.get("STOCK_PROVIDER")) == "live":
    from .services import LiveStockPriceService as StockPriceService
else:
    from .services import LocalStockPriceService as StockPriceService


@login_required(login_url="accounts:page-login")
def stocks_page(request: HttpRequest) -> HttpResponse:
    return render(request, "finance/stocks_page.html")


@login_required(login_url="accounts:page-login")
def stocks_api(request: HttpRequest, symbol: str) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    today = datetime.today()
    last_30_days = today - timedelta(days=30)
    try:
        image_data = StockPriceService().create_price_plot(
            symbol,
            last_30_days.strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d"),
        )
        return render(
            request, "finance/stock_price_plot.html", {"image_data": image_data}
        )
    except:
        return HttpResponseServerError("Failed to load stock prices")
