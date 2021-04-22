from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('first name'), max_length=200, blank=True)
    last_name = models.CharField(_('last name'), max_length=200, blank=True)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.get_full_name() or self.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    avatar_url = models.URLField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
