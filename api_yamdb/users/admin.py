from django.contrib import admin

from .models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'bio', 'role')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


admin.site.register(User)
