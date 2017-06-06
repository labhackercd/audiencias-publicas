from django.contrib import admin
from apps.accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin')
    list_filter = ['user', 'is_admin']


admin.site.register(UserProfile, UserProfileAdmin)
