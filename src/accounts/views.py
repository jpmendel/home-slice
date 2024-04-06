from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
)


def login_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    return render(request, "accounts/login_page.html")


def login_action(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    body = request.POST
    username = body["username"]
    password = body["password"]

    if username is None or password is None:
        return HttpResponseBadRequest("Invalid username or password")

    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseBadRequest("Invalid username or password")

    login(request=request, user=user)
    response = HttpResponse()
    response["HX-Redirect"] = reverse("posts:posts-page")
    return response


@login_required(login_url="accounts:login-page")
def logout_action(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    logout(request=request)
    response = HttpResponse()
    response["HX-Redirect"] = reverse("accounts:login-page")
    return response


def user_api(request: HttpRequest, username: str | None = None) -> HttpResponse:
    if request.method == "POST":
        return create_user(request)
    if request.method == "DELETE":
        return delete_user(request, username)
    return HttpResponseNotAllowed(["POST", "DELETE"])


def create_user(request: HttpRequest) -> HttpResponse:
    body = request.POST
    username = body["username"]
    password = body["password"]

    if username is None or password is None:
        return HttpResponseBadRequest("Username and password required")

    if "isAdmin" in body and body["isAdmin"]:
        User.objects.create_superuser(
            username=username,
            password=password,
            email=None,
        )
    else:
        User.objects.create_user(
            username=username,
            password=password,
        )
    return HttpResponse()


def delete_user(_request: HttpRequest, username: str | None) -> HttpResponse:
    if username is None:
        return HttpResponseBadRequest("Must provide username to delete")

    try:
        user = User.objects.get(username=username)
        user.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest(f'User with username "{username}" not found')
