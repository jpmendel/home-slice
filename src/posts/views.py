from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseNotAllowed,
    QueryDict,
)
from .models import Post


@login_required
def posts_page(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "posts/posts_page.html", {"title": "Posts"})


@login_required
def start_edit_post(request: HttpRequest, post_id: Optional[int]) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponseNotFound(f'Post with ID "{post_id}" not found')
    return render(request, "posts/edit_post_form.html", {"post": post})


@login_required
def cancel_edit_post(request: HttpRequest, post_id: Optional[int]) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponseNotFound(f'Post with ID "{post_id}" not found')
    return render(request, "posts/post_content.html", {"post": post})


@login_required
def posts_api(request: HttpRequest, post_id: Optional[int] = None) -> HttpResponse:
    if request.method == "GET":
        return get_posts(request, post_id)
    if request.method == "POST":
        return create_post(request)
    if request.method == "PATCH":
        return update_post(request, post_id)
    if request.method == "DELETE":
        return delete_post(request, post_id)
    return HttpResponseNotAllowed(["GET", "POST", "PATCH", "DELETE"])


def get_posts(request: HttpRequest, post_id: Optional[int] = None) -> HttpResponse:
    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
        except:
            return HttpResponseNotFound(f'Post with id "{post_id}" not found')
        return render(request, "posts/post_content.html", {"post": post})

    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/posts_list.html", {"posts": posts})


def create_post(request: HttpRequest) -> HttpResponse:
    content = request.POST.get("content")
    if content is None:
        return HttpResponseBadRequest("Post requires content to create")

    user = request.user
    post = Post.objects.create(author=user, content=content)
    return render(request, "posts/post_content.html", {"post": post})


def update_post(request: HttpRequest, post_id: Optional[int] = None) -> HttpResponse:
    if post_id is None:
        return HttpResponseBadRequest("Post ID is required to update")

    body = QueryDict(request.body)
    content = body.get("content")
    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponseNotFound(f'User with username "{post_id}" not found')
    if content is not None and content != post.content:
        post.content = content
        post.updated_at = datetime.now(ZoneInfo("UTC"))
    post.save()
    return render(request, "posts/post_content.html", {"post": post})


def delete_post(request: HttpRequest, post_id: Optional[int] = None) -> HttpResponse:
    if post_id is None:
        return HttpResponseBadRequest("Post ID is required to delete")

    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponseNotFound(f'User with username "{post_id}" not found')
    post.delete()
    return HttpResponse()
