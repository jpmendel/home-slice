from typing import Optional
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from .apps import LightsConfig
from .services.light_strip import LightStripService


def light_strip_service() -> LightStripService:
    config = apps.get_app_config("lights")
    assert isinstance(config, LightsConfig)
    return config.light_strip_service


@login_required
def lights_page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "lights/lights_page.html")


@login_required
def add_light_pattern_step(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    index = int(request.GET.get("index", 0))
    return render(request, "lights/color_pattern_step_form.html", {"index": index + 1})


@login_required
def set_light_pattern(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    return HttpResponse()


@login_required
def clear_lights(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        light_strip_service().clear_color()
        return HttpResponse()
    except:
        return HttpResponseServerError("An error occurred")


@login_required
def add_light_animation(request: HttpRequest) -> HttpResponse:
    # TODO: Implement
    return HttpResponse()


@login_required
def play_light_animation(request: HttpRequest) -> HttpResponse:
    # TODO: Implement
    return HttpResponse()
