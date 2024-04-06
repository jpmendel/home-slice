from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.posts_page, name="page-posts"),
    path("api/post", views.posts_api, name="api-posts"),
    path("api/post/<int:post_id>", views.posts_api, name="api-posts-one"),
    path(
        "api/post/create/start",
        views.start_create_post,
        name="api-posts-create-start",
    ),
    path(
        "api/post/create/cancel",
        views.cancel_create_post,
        name="api-posts-create-cancel",
    ),
    path(
        "api/post/<int:post_id>/edit/start",
        views.start_edit_post,
        name="api-posts-edit-start",
    ),
    path(
        "api/post/<int:post_id>/edit/cancel",
        views.cancel_edit_post,
        name="api-posts-edit-cancel",
    ),
]
