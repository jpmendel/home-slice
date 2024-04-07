from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.posts_page, name="page-posts"),
    path("api/posts", views.posts_api, name="api-posts"),
    path("api/posts/<int:post_id>", views.posts_api, name="api-posts-one"),
    path(
        "api/posts/create/start",
        views.start_create_post,
        name="api-posts-create-start",
    ),
    path(
        "api/posts/create/cancel",
        views.cancel_create_post,
        name="api-posts-create-cancel",
    ),
    path(
        "api/posts/<int:post_id>/edit/start",
        views.start_edit_post,
        name="api-posts-edit-start",
    ),
    path(
        "api/posts/<int:post_id>/edit/cancel",
        views.cancel_edit_post,
        name="api-posts-edit-cancel",
    ),
]
