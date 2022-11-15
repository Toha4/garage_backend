from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("authentication.urls")),
    path("", include("core.urls")),
    path("", include("orders.urls")),
    path("", include("warehouse.urls")),
    path("", include("reports.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
