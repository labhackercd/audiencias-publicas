from django.conf.urls import url
from apps.core.views import HomeView, VideoDetail
from apps.core.api import (api_root, AgendaListAPI, MessageListAPI,
                           QuestionListAPI, VideoListAPI, VoteListAPI)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^salas/(?P<pk>\d+)/',
        VideoDetail.as_view(), name='video_room'),
]

urlpatterns += [
    url(r'^api/$', api_root),
    url(r'^api/agenda/$', AgendaListAPI.as_view(),
        name='agenda_list_api'),
    url(r'^api/messages/$', MessageListAPI.as_view(),
        name='message_list_api'),
    url(r'^api/question/$', QuestionListAPI.as_view(),
        name='question_list_api'),
    url(r'^api/video/$', VideoListAPI.as_view(),
        name='video_list_api'),
    url(r'^api/vote/$', VoteListAPI.as_view(),
        name='vote_list_api'),
]
