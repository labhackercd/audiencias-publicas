import pytest
from mixer.backend.django import mixer
from apps.accounts.models import User, UserProfile


class TestAccounts():

    def test_apps(self):
        from apps.accounts.apps import AccountsConfig
        assert AccountsConfig.name == 'apps.accounts'

    @pytest.mark.django_db
    def test_create_user(self):
        user = mixer.blend(
            User, is_active=True, first_name='test', last_name='user')
        assert User.objects.count() == 1
        assert user.__str__() == 'test user'

    @pytest.mark.django_db
    def test_create_profile(self):
        user = mixer.blend(User, is_active=True)
        UserProfile.objects.create(user=user, is_admin=True)
        assert UserProfile.objects.count() == 1
