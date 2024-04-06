from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.posts_page, name="posts-page"),
    path("api/post", views.posts_api, name="posts-api"),
    path("api/post/<int:post_id>", views.posts_api, name="posts-api-one"),
    path(
        "api/post/create/start",
        views.start_post,
        name="start-create-post-api",
    ),
    path(
        "api/post/create/cancel",
        views.cancel_create_post,
        name="cancel-create-post-api",
    ),
    path(
        "api/post/<int:post_id>/edit/start",
        views.start_edit_post,
        name="start-edit-post-api",
    ),
    path(
        "api/post/<int:post_id>/edit/cancel",
        views.cancel_edit_post,
        name="cancel-edit-post-api",
    ),
]
