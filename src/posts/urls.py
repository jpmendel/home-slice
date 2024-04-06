from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.posts_page, name="posts-page"),
    path("posts/create", views.create_post_page, name="create-post-page"),
    path("api/post", views.posts_api, name="posts-api"),
    path("api/post/<int:post_id>", views.posts_api, name="posts-api-one"),
]
