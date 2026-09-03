from django.contrib import admin
from .models import Message

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'sent_on',
        'user',
        'course',
        'content'
    ]
    list_filter = [
        'sent_on',
        'course',
    ]
    search_fields = [
        'content',
    ]
    raw_id_fields = [
        'user',
    ]
admin.site.register(Message, MessageAdmin)