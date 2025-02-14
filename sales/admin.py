from django.contrib import admin
from .import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'name']

@admin.register(models.FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(models.FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ['form', 'label', 'field_type', 'choices', 'required']
    list_select_related = ['form']

@admin.register(models.FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ['contact', 'form', 'response_data', 'submitted_at']
