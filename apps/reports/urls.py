from django.conf.urls import url
from apps.reports import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/new-users', api.NewUsersViewSet)
router.register(r'api/votes', api.VotesReportViewSet)

urlpatterns = router.urls
urlpatterns += [
    url(r'^api/$', api.api_reports_root, name='reports_api_root'),
]
