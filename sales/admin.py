from django.contrib import admin
from .models import Contact
from adminsortable.admin import SortableAdmin
# Register your models here.
@admin.register(Contact)
class Contact(SortableAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'company', 'date']
    