from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from apps.core import urls as core_urls
from rest_framework.authtoken.models import Token
from django_q.models import Success, Failure, Schedule


if settings.URL_PREFIX:
    prefix = r'^%s/' % (settings.URL_PREFIX)
else:
    prefix = r'^'

urlpatterns = [
    url(prefix + r'', include(core_urls)),
    url(prefix + r'admin/', include(admin.site.urls)),
]

admin.site.unregister(Token)
admin.site.unregister(Success)
admin.site.unregister(Failure)
admin.site.unregister(Schedule)

admin.site.site_header = 'Audiências Públicas Interativas'
