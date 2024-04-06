from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_page, name="page-login"),
    path("api/login", views.login_action, name="api-login"),
    path("api/logout", views.logout_action, name="api-logout"),
    path("api/user", views.user_api, name="api-user"),
    path("api/user/<str:username>", views.user_api, name="api-user-one"),
]
