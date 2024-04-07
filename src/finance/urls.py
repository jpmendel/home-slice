from django.urls import path
from . import views

urlpatterns = [
    path("stocks", views.stocks_page, name="page-stocks"),
    path("api/stocks/<str:symbol>", views.stocks_api, name="api-stocks"),
]
