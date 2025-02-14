from django.contrib import admin
from .models import Contact
from adminsortable.models import Sortable

# Register your models here.
@admin.register(models.Contact)
class Contact(SortableAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'company', 'date']
    