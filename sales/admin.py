from django.contrib import admin
from .import models


@admin.register(models.ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'message']
