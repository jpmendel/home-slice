from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponseRedirect(reverse("posts:page-posts"))


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("", include(("posts.urls", "posts"), namespace="posts")),
    path("", include(("lights.urls", "lights"), namespace="lights")),
    path("", include(("finance.urls", "finance"), namespace="finance")),
    path("", home, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
