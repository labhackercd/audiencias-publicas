from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.get_full_name() or self.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    avatar_url = models.URLField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
