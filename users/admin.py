from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'chat_id',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
        'password',
    )
    list_filter = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'email', 'chat_id',)
