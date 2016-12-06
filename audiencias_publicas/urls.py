from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from apps.accounts import urls as accounts_urls
from apps.core import urls as core_urls

if settings.URL_PREFIX:
    prefix = r'^%s/' % (settings.URL_PREFIX)
else:
    prefix = r'^'

urlpatterns = [
    url(prefix + r'', include(core_urls)),
    url(prefix + r'', include(accounts_urls)),
    url(prefix + r'admin/', include(admin.site.urls)),
]
