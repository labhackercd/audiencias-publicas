from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth import get_user_model
import json

UserModel = get_user_model()


class AudienciasAuthBackend(RemoteUserBackend):

    def authenticate(self, request, remote_user):
        if not remote_user:
            return
        user = None
        remote_user_data = json.loads(
            request.META.get('HTTP_REMOTE_USER_DATA')
        )
        user, _ = UserModel.objects.get_or_create(
            email=remote_user_data['email']
        )
        user.username = remote_user
        user.first_name = remote_user_data['first_name']
        user.last_name = remote_user_data['last_name']
        user.save()

        return user
