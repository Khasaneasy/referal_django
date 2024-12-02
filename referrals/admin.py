from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code',
                    'activated_invite_code', 'invited_by', 'is_active')
    search_fields = ('phone_number',)
    list_filter = ('is_active',)
    ordering = ('phone_number',)

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'invite_code', 'activated_invite_code',
                       'invited_by', 'is_active')
        }),
    )