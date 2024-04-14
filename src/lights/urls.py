from django.urls import path
from . import views

urlpatterns = [
    path("lights", views.lights_page, name="page-lights"),
    path(
        "api/lights/pattern/add",
        views.add_light_pattern_step,
        name="api-lights-pattern-add",
    ),
    path(
        "api/lights/pattern/set",
        views.set_light_pattern,
        name="api-lights-pattern-set",
    ),
    path(
        "api/lights/anim/add",
        views.add_light_animation,
        name="api-lights-anim-add",
    ),
    path(
        "api/lights/anim/play",
        views.play_light_animation,
        name="api-lights-anim-play",
    ),
    path("api/lights/clear", views.clear_lights, name="api-lights-clear"),
]
