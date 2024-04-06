from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_page, name="login-page"),
    path("api/login", views.login_action, name="login-api"),
    path("api/logout", views.logout_action, name="logout-api"),
    path("api/user", views.user_api, name="user-api"),
    path("api/user/<str:username>", views.user_api, name="user-api-one"),
]
