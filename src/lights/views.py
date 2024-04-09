from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import HttpRequest, HttpResponse
from .apps import LightsConfig
from .services.light_strip import LightStripService


def light_strip_service() -> LightStripService:
    config = apps.get_app_config("lights")
    assert isinstance(config, LightsConfig)
    return config.light_strip_service


@login_required
def lights_page(request: HttpRequest) -> HttpResponse:
    return render(request, "lights/lights_page.html")
