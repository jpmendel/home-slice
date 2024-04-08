from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import HttpRequest, HttpResponse
from .services.light_strip import LightStripService


def light_strip_service() -> LightStripService:
    config = apps.get_app_config("lights")
    return config.light_strip_service  # type: ignore


@login_required(login_url="accounts:page-login")
def lights_page(request: HttpRequest) -> HttpResponse:
    return render(request, "lights/lights_page.html")
