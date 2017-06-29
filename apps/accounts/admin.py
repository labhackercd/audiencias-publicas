from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import UserProfile, User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin')
    list_filter = ['user', 'is_admin']


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
