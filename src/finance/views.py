import os
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)

if str(os.environ.get("STOCKS_PROVIDER")) == "live":
    from .services import LiveStockPriceService as StockPriceService
else:
    from .services import LocalStockPriceService as StockPriceService


@login_required(login_url="accounts:page-login")
def stocks_page(request: HttpRequest) -> HttpResponse:
    return render(request, "finance/stocks_page.html")


@login_required(login_url="accounts:page-login")
def stocks_api(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    symbol = request.GET.get("symbol")
    if symbol is None or symbol == "":
        return HttpResponseBadRequest("Must provide stock symbol")
    symbol = symbol.upper()

    today = datetime.today()
    last_30_days = today - timedelta(days=30)
    try:
        image_data = StockPriceService().create_price_plot(symbol, last_30_days, today)
        return render(
            request, "finance/stock_price_plot.html", {"image_data": image_data}
        )
    except:
        return HttpResponseServerError("Failed to load stock prices")
