from django.contrib import admin
from .import models

# Register your models here.
@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'content', 'timestamp']
    list_select_related = ['user']
    list_per_page = 20
