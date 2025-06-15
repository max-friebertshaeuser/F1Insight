from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="F1Insight API",
        default_version='v1',
        description="API documentation for F1Insight",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ],
)

urlpatterns = [
    path('api/auth/', include('user_auth.urls')),
    path('admin/', admin.site.urls),
    path('api/catalog/', include('catalog.urls')),
    path('api/betting/', include(('betting.urls', 'betting'), namespace='betting')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
