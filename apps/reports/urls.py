from django.conf.urls import url
from apps.reports import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/new-users', api.NewUsersViewSet)
router.register(r'api/votes', api.VotesReportViewSet)
router.register(r'api/rooms', api.RoomsReportViewSet)
router.register(r'api/questions', api.QuestionsReportViewSet)
router.register(r'api/messages', api.MessagesReportViewSet)
router.register(r'api/participants', api.ParticipantsReportViewSet)
router.register(r'api/ranking', api.RoomRankingViewSet)

urlpatterns = router.urls
urlpatterns += [
    url(r'^api/$', api.api_reports_root, name='reports_api_root'),
]
