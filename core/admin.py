from django.contrib import admin
from .models import Item, Message


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'report_type',
        'category',
        'location',
        'status',
        'user',
        'event_date',
    )

    list_filter = (
        'report_type',
        'category',
        'status',
        'location'
    )

    search_fields = (
        'title',
        'description',
        'location'
    )

    ordering = (
        '-created_at',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'receiver',
        'item',
        'content',
        'created_at',
        'is_read'
    )
    list_filter = (
        'is_read',
        'created_at'
    )
    search_fields = (
        'content',
        'sender__username',
        'receiver__username',
        'item__title'
    )
    ordering = (
        '-created_at',
    )