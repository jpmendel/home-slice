from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
)
from .apps import LightsConfig
from .services.light_strip import LightStripService
from .util import color_from_hue, pattern_from_colors


def light_strip_service() -> LightStripService:
    config = apps.get_app_config("lights")
    assert isinstance(config, LightsConfig)
    return config.light_strip_service


@login_required
def lights_page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "lights/lights_page.html", {"title": "Lights"})


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
    colors = request.POST.getlist("color[]")
    if colors is None or len(colors) == 0:
        return HttpResponseBadRequest("Missing info")
    if len(colors) == 1:
        hue = int(colors[0])
        r, g, b = color_from_hue(hue)
        light_strip_service().set_solid_color(r, g, b)
    else:
        pattern = pattern_from_colors(colors)
        light_strip_service().set_pattern(pattern)
    return HttpResponse()


@login_required
def clear_lights(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    light_strip_service().clear_color()
    return render(request, "lights/color_pattern_step_form.html", {"index": 0})


@login_required
def add_light_animation(request: HttpRequest) -> HttpResponse:
    # TODO: Implement
    return HttpResponse()


@login_required
def play_light_animation(request: HttpRequest) -> HttpResponse:
    # TODO: Implement
    return HttpResponse()
