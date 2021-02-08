from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from apps.core import urls as core_urls
from apps.notification import urls as notification_urls
from apps.reports import urls as reports_urls
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


if settings.URL_PREFIX:
    prefix = r'^%s/' % (settings.URL_PREFIX)
else:
    prefix = r'^'

schema_view = get_schema_view(
    openapi.Info(
        title="Audiências Interativas API",
        default_version='v1',
        description="Este projeto tem como finalidade servir dados para um \
                    dashboard que possibilitará aos servidores da CPP \
                    acompanhar como está a participação dos usuários nas \
                    ferramentas da Câmara",
        contact=openapi.Contact(email="labhacker@camara.leg.br"),
        license=openapi.License(name="GNU General Public License v3.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(prefix + r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(prefix + r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(prefix + r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    url(prefix + r'', include(core_urls)),
    url(prefix + r'notification/', include(notification_urls)),
    url(prefix + r'admin/', include(admin.site.urls)),
    url(prefix + r'reports/', include(reports_urls)),
]

admin.site.unregister(Token)

admin.site.site_header = 'Audiências Públicas Interativas'
