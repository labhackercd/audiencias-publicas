from django.conf.urls import include, url
from django.contrib import admin
from apps.core import urls as core_urls

urlpatterns = [
    url(r'^', include(core_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
