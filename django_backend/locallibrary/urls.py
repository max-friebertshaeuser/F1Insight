# django_backend/urls.py
from django.contrib import admin
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.urls import path


@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
]
