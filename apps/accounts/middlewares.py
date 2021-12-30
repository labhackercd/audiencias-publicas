from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import get_user_model, load_backend
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from apps.accounts.models import UserProfile
from apps.accounts.backends import AudienciasAuthBackend
import json

User = get_user_model()


class AudienciasRemoteUser(RemoteUserMiddleware):
    header = "HTTP_AUTH_USER"
    force_logout_if_no_header = False
    # Override process request to pass the request to authentication method
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(request, remote_user=username)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            user_data = json.loads(request.META['HTTP_REMOTE_USER_DATA'])
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.username = username
            if not hasattr(user, 'profile'):
                profile = UserProfile()
                profile.user = user
            else:
                profile = user.profile
            profile.avatar_url = user_data['avatar']
            profile.save()
            user.save()

            request.user = user
            auth.login(request, user)

    def _remove_invalid_user(self, request):
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
            raise
        else:
            if isinstance(stored_backend, AudienciasAuthBackend):
                auth.logout(request)