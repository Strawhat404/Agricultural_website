from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Agriconnect API",
        default_version='v1',
        description="API documentation for Agriconnect platform",
        terms_of_service="https://www.agriconnect.com/terms/",
        contact=openapi.Contact(email="contact@agriconnect.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        # Authentication
        path('auth/', include('dj_rest_auth.urls')),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
        
        # Apps
        path('users/', include('apps.users.urls')),
        path('marketplace/', include('apps.marketplace.urls')),
        path('weather/', include('apps.weather.urls')),
        path('news/', include('apps.news.urls')),
        path('advisory/', include('apps.advisory.urls')),
        path('payments/', include('apps.payments.urls')),
        path('logistics/', include('apps.logistics.urls')),
        path('analytics/', include('apps.analytics.urls')),
        
        # API Documentation
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ])),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 