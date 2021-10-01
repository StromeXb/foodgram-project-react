from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe

User = get_user_model()


class ManualUser(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(User, ManualUser)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Страница админ. панели подписок."""

    list_display = ('pk', 'subscriber', 'author')
    search_fields = ('subscriber', 'author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'
