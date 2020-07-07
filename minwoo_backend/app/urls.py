from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/main/', admin.site.urls, name='admin'),
    path('', include('user.urls', namespace='user')),
    path('', include('board.urls', namespace='board')),
    path('', include('information.urls', namespace='information')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'drf_yasg' in settings.INSTALLED_APPS:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Big Step API",
            default_version='v1',
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = urlpatterns + [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
