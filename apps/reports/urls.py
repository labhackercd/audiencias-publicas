from django.conf.urls import url
from apps.reports import views

urlpatterns = [
    url(r'^data/$', views.initial_view, name='initial_view'),
]
