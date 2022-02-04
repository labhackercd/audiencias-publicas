from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.routers import DefaultRouter
from apps.core.views import (VideoDetail, RoomQuestionList, ClosedVideos,
                             QuestionDetail, index, redirect_to_room,
                             RoomReportView, set_answer_time, set_answered,
                             set_priotity, WidgetVideoDetail, create_attachment,
                             delete_attachment, add_external_link,
                             remove_external_link, create_video_attachment,
                             delete_video, order_videos, censorship)
from apps.core import api


urlpatterns = [
    path('', index, name='home'),
    path('pergunta/<int:pk>/', QuestionDetail.as_view(),
         name='question_detail'),
    path('pergunta/<int:question_id>/definir_resposta/', set_answer_time,
         name='set_question_answer_time'),
    path('pergunta/<int:question_id>/respondida/', set_answered,
         name='set_question_answered'),
    path('pergunta/<int:question_id>/prioritaria/', set_priotity,
         name='set_question_priotity'),
    path('sala/<int:pk>/', VideoDetail.as_view(), name='video_room'),
    path('sala/<int:room_id>/anexo/adicionar/', create_attachment,
         name='create_attachment'),
    path('anexo/<int:attachment_id>/deletar/', delete_attachment,
         name='delete_attachment'),
    path('sala/<int:room_id>/video/adicionar/', create_video_attachment,
         name='create_video_attachment'),
    path('video/<int:video_id>/deletar/', delete_video,
         name='delete_video'),
    path('sala/<int:room_id>/link/adicionar/', add_external_link,
         name='add_external_link'),
    path('sala/<int:room_id>/link/deletar/', remove_external_link,
         name='remove_external_link'),
    path('sala/<int:pk>/relatorio/', RoomReportView.as_view(),
         name='room_report'),
    path('sala/reuniao/<int:cod_reunion>/', redirect_to_room,
         name='video_reunion_room'),
    path('sala/<int:pk>/perguntas/', RoomQuestionList.as_view(),
         name='questions_list'),
    path('sala/<int:room_id>/ordered-videos/', order_videos,
         name='order_videos'),
    path('fechadas/', ClosedVideos.as_view(), name='video_list'),
    path('widget/<int:pk>/',
         ensure_csrf_cookie(WidgetVideoDetail.as_view()),
         name='widget_index'),
    path('blacklist/', censorship, name='censorship')
]

router = DefaultRouter()
router.register(r'api/user', api.UserViewSet)
router.register(r'api/message', api.MessageViewSet)
router.register(r'api/question', api.QuestionViewSet)
router.register(r'api/room', api.RoomViewSet)
router.register(r'api/vote', api.VoteViewSet)

urlpatterns += router.urls
urlpatterns += [
    path('api/', api.api_root, name='api_root'),
]
