from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin
from django.urls import path, re_path, include

service_name = "moneta"

urlpatterns = [
    re_path(settings.STATIC_URL[1:] + r"(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path(f'{service_name}/admin/', admin.site.urls),
    path(f'{service_name}/user/', include('users.urls')),
    path(f'{service_name}/expense/', include('expenses.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Admin
admin.site.site_header = "Moneta (Track Your Expense)"
admin.site.index_title = "Moneta (Track Your Expense)"
admin.site.site_title = "Moneta (Track Your Expense)"