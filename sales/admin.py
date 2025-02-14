from django.contrib import admin
from .models import DynamicField
from adminsortable.admin import SortableAdmin


# Register your models here.
@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'required', 'sales_team')
    list_filter = ('field_type', 'sales_team')



# @admin.register(Contact)
# class Contact(SortableAdmin):
#     list_display = ['name', 'email', 'phone', 'message', 'company', 'date']
    