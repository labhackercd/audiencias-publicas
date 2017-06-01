from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.core.views import (VideoDetail, RoomQuestionList, ClosedVideos,
                             VideoReunionDetail, QuestionDetail, index,
                             RoomReportView, set_answer_time, set_answered,
                             WidgetVideoDetail)
from apps.core.api import (api_root, MessageListAPI, QuestionListAPI,
                           VoteListAPI, UserListAPI, RoomAPI, RoomListAPI)


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^pergunta/(?P<pk>\d+)/?$', QuestionDetail.as_view(),
        name='question_detail'),
    url(r'^pergunta/(?P<question_id>\d+)/definir_resposta/?$', set_answer_time,
        name='set_question_answer'),
    url(r'^pergunta/(?P<question_id>\d+)/respondida/?$', set_answered,
        name='set_question_answered'),
    url(r'^sala/(?P<pk>\d+)/?$', VideoDetail.as_view(), name='video_room'),
    url(r'^sala/(?P<pk>\d+)/relatorio/?$', RoomReportView.as_view(),
        name='room_report'),
    url(r'^sala/reuniao/(?P<cod_reunion>\d+)/?$', VideoReunionDetail.as_view(),
        name='video_reunion_room'),
    url(r'^sala/(?P<pk>\d+)/perguntas/?$', RoomQuestionList.as_view(),
        name='questions_list'),
    url(r'^fechadas/?$', ClosedVideos.as_view(), name='video_list'),
    url(r'^widget/(?P<pk>\d+)/?$',
        ensure_csrf_cookie(WidgetVideoDetail.as_view()),
        name='widget_index'),
]

urlpatterns += [
    url(r'^api/$', api_root),
    url(r'^api/messages/$', MessageListAPI.as_view(), name='message_list_api'),
    url(r'^api/question/$', QuestionListAPI.as_view(),
        name='question_list_api'),
    url(r'^api/room/$', RoomListAPI.as_view(), name='room_list_api'),
    url(r'^api/room/(?P<pk>\d+)$', RoomAPI.as_view(),
        name='room_detail_api'),
    url(r'^api/vote/$', VoteListAPI.as_view(), name='vote_list_api'),
    url(r'^api/user/$', UserListAPI.as_view(), name='user_list_api'),
]
