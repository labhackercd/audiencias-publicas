from django.conf.urls import url
from apps.core.views import (VideoDetail, RoomQuestionList, QuestionDetail,
                             receive_callback, index)
from apps.core.api import (api_root, AgendaListAPI, MessageListAPI,
                           QuestionListAPI, VideoListAPI, VoteListAPI)

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^pergunta/(?P<pk>\d+)/?$', QuestionDetail.as_view(),
        name='question_detail'),
    url(r'^sala/(?P<pk>\d+)/?$', VideoDetail.as_view(), name='video_room'),
    url(r'^sala/(?P<pk>\d+)/perguntas/?$', RoomQuestionList.as_view(),
        name='questions_list'),
    url(r'^notification/callback/?$', receive_callback,
        name='receive_callback'),
]

urlpatterns += [
    url(r'^api/$', api_root),
    url(r'^api/agenda/$', AgendaListAPI.as_view(), name='agenda_list_api'),
    url(r'^api/messages/$', MessageListAPI.as_view(), name='message_list_api'),
    url(r'^api/question/$', QuestionListAPI.as_view(),
        name='question_list_api'),
    url(r'^api/video/$', VideoListAPI.as_view(), name='video_list_api'),
    url(r'^api/vote/$', VoteListAPI.as_view(), name='vote_list_api'),
]
