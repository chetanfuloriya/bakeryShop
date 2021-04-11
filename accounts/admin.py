from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth import get_user_model

from accounts.models import Order


@admin.register(get_user_model())
class UserAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'first_name', 'last_name', 'user_type',)
    search_fields = (
        'first_name', 'last_name', 'mobile', 'email',
    )
    readonly_fields = ('created_at', 'modified_at')
    list_filter = ('user_type', 'is_active')


@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'user', 'actual_price', 'discount')
    search_fields = (
        'user__id', 'user__email', 'user__mobile',
    )
    readonly_fields = ('created_at', 'modified_at')
    raw_id_fields = ('user',)
