from django.urls import path
from . import views

urlpatterns = [
    path("lights", views.lights_page, name="page-lights"),
]
