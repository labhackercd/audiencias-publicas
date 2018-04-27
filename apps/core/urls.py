from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.core.views import (VideoDetail, RoomQuestionList, ClosedVideos,
                             QuestionDetail, index, redirect_to_room,
                             RoomReportView, set_answer_time, set_answered,
                             set_priotity, WidgetVideoDetail, create_attachment,
                             delete_attachment, add_external_link,
                             remove_external_link, create_video_attachment,
                             delete_video)
from apps.core.api import (api_root, MessageListAPI, QuestionListAPI,
                           VoteListAPI, UserListAPI, RoomAPI, RoomListAPI)


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^pergunta/(?P<pk>\d+)/?$', QuestionDetail.as_view(),
        name='question_detail'),
    url(r'^pergunta/(?P<question_id>\d+)/definir_resposta/?$', set_answer_time,
        name='set_question_answer_time'),
    url(r'^pergunta/(?P<question_id>\d+)/respondida/?$', set_answered,
        name='set_question_answered'),
    url(r'^pergunta/(?P<question_id>\d+)/prioritaria/?$', set_priotity,
        name='set_question_priotity'),
    url(r'^sala/(?P<pk>\d+)/?$', VideoDetail.as_view(), name='video_room'),
    url(r'^sala/(?P<room_id>\d+)/anexo/adicionar/?$', create_attachment,
        name='create_attachment'),
    url(r'^anexo/(?P<attachment_id>\d+)/deletar/?$', delete_attachment,
        name='delete_attachment'),
    url(r'^sala/(?P<room_id>\d+)/video/adicionar/?$', create_video_attachment,
        name='create_video_attachment'),
    url(r'^video/(?P<video_id>\d+)/deletar/?$', delete_video,
        name='delete_video'),
    url(r'^sala/(?P<room_id>\d+)/link/adicionar/?$', add_external_link,
        name='add_external_link'),
    url(r'^sala/(?P<room_id>\d+)/link/deletar/?$', remove_external_link,
        name='remove_external_link'),
    url(r'^sala/(?P<pk>\d+)/relatorio/?$', RoomReportView.as_view(),
        name='room_report'),
    url(r'^sala/reuniao/(?P<cod_reunion>\d+)/?$', redirect_to_room,
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
