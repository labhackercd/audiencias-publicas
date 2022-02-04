from django.urls import path
from apps.notification.views import send_participants_notification


urlpatterns = [
    path('participants/<int:room_id>/', send_participants_notification,
         name='participants_notification'),
]
