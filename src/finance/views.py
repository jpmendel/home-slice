from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from .apps import FinanceConfig
from .services import StockPriceService


def stock_price_service() -> StockPriceService:
    config = apps.get_app_config("finance")
    assert isinstance(config, FinanceConfig)
    return config.stock_price_service


@login_required
def stocks_page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "finance/stocks_page.html", {"title": "Finance"})


@login_required
def stocks_api(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    symbol = request.GET.get("symbol")
    if symbol is None or symbol == "":
        return HttpResponseBadRequest("Must provide stock symbol")
    symbol = symbol.upper()

    tz = ZoneInfo("America/New_York")
    today = datetime.now(tz)
    last_30_days = today - timedelta(days=30)
    try:
        image_data = stock_price_service().create_price_plot(
            symbol,
            last_30_days,
            today,
        )
        return render(
            request, "finance/stock_price_plot.html", {"image_data": image_data}
        )
    except:
        return HttpResponseServerError("Failed to load stock prices")
