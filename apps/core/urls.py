from django.conf.urls import url
from apps.core.views import HomeView, VideoDetail

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^salas/(?P<slug>[\w_-]+)-(?P<pk>\d+)/', VideoDetail.as_view(), name='video_room'),
]
