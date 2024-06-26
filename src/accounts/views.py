from typing import Optional
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.urls import reverse, resolve
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)


def login_page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    return render(request, "accounts/login_page.html")


def settings_page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "accounts/settings_page.html", {"title": "Settings"})


def login_action(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    body = request.POST
    username = body.get("username")
    password = body.get("password")
    next_page = body.get("next")

    if username is None or password is None:
        return HttpResponseBadRequest("Invalid username or password")

    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseBadRequest("Invalid username or password")
    login(request=request, user=user)

    next_url: Optional[str] = None
    if next_page:
        try:
            next_url = next_page if resolve(next_page) else None
        except:
            pass
    response = HttpResponse()
    response["HX-Redirect"] = next_url or reverse("home")
    return response


@login_required
def logout_action(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    logout(request=request)
    response = HttpResponse()
    response["HX-Redirect"] = reverse("accounts:page-login")
    return response


@login_required
def user_api(request: HttpRequest, username: Optional[str] = None) -> HttpResponse:
    if request.method == "POST":
        return create_user(request)
    if request.method == "DELETE":
        return delete_user(request, username)
    return HttpResponseNotAllowed(["POST", "DELETE"])


def create_user(request: HttpRequest) -> HttpResponse:
    body = request.POST
    username = body.get("username")
    password = body.get("password")

    if username is None or password is None:
        return HttpResponseBadRequest("Username and password required")

    try:
        if "isAdmin" in body and body.get("isAdmin"):
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
    except IntegrityError:
        return HttpResponseBadRequest(f'User with name "{username}" already exists')
    except:
        return HttpResponseServerError("An unknown error occurred")
    return HttpResponse()


def delete_user(request: HttpRequest, username: Optional[str]) -> HttpResponse:
    if username is None:
        return HttpResponseBadRequest("Username must be provided to delete")

    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponseNotFound(f'User with username "{username}" not found')
    user.delete()
    return HttpResponse()
