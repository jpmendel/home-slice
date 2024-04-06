from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
)
from .models import Post


@login_required(login_url="accounts:login-page")
def posts_page(request: HttpRequest) -> HttpResponse:
    return render(request, "posts/posts_page.html")


@login_required(login_url="accounts:login-page")
def create_post_page(request: HttpRequest) -> HttpResponse:
    return render(request, "posts/create_post_page.html")


@login_required(login_url="accounts:login-page")
def posts_api(request: HttpRequest, post_id: int | None = None) -> HttpResponse:
    if request.method == "GET":
        return get_posts(request, post_id)
    if request.method == "POST":
        return create_post(request)
    if request.method == "PUT":
        return update_post(request, post_id)
    if request.method == "DELETE":
        return delete_post(request, post_id)
    return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])


def get_posts(request: HttpRequest, post_id: int | None = None) -> HttpResponse:
    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
            return render(request, "posts/post_content.html", {"post": post})
        except:
            return HttpResponseBadRequest(f'Post with id "{post_id}" does not exist')

    posts = Post.objects.all()
    return render(request, "posts/posts_list.html", {"posts": posts})


def create_post(request: HttpRequest) -> HttpResponse:
    content = request.POST["content"]
    if content is None:
        return HttpResponseBadRequest("Post requires content to create")

    user = request.user
    Post.objects.create(user=user, content=content)

    response = HttpResponse()
    response["HX-Redirect"] = reverse("posts:posts-page")
    return response


def update_post(request: HttpRequest, post_id: int | None = None) -> HttpResponse:
    if post_id is None:
        return HttpResponseBadRequest("Must provide post ID to update")

    try:
        post = Post.objects.get(id=post_id)
        if "content" in request.POST:
            post.content = request.POST["content"]
        post.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest(f'User with username "{post_id}" not found')


def delete_post(request: HttpRequest, post_id: int | None = None) -> HttpResponse:
    if post_id is None:
        return HttpResponseBadRequest("Must provide post ID to delete")

    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest(f'User with username "{post_id}" not found')
