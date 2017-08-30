from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import UserProfile, User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin')
    list_filter = ['is_admin', 'user__is_superuser']
    search_fields = (
        'user__first_name', 'user__last_name', 'user__email', 'user__username')


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
