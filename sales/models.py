from adminsortable.models import Sortable,SortableMixin
from home.models import CustomUser as User
from django.apps import apps
from django.db import models


# Predefined Field Types for Selection
FIELD_TYPES = {
    'text': models.TextField(help_text='Text Area'),
    'file': models.FileField(help_text='Files to upload'),
    'images': models.ImageField(upload_to='uploads/sales'),
    'char': models.CharField(max_length=255, help_text='Short Text'),
    'email': models.EmailField(help_text='Email Address'),
    'phone': models.CharField(max_length=15, help_text='Phone Number'),
    'date': models.DateField(auto_now_add=True, help_text='Date Field'),
    'datetime': models.DateTimeField(auto_now_add=True, help_text='DateTime Field'),
    'checkbox': models.BooleanField(default=False, help_text='Checkbox Field'),
    'choices': models.CharField(max_length=255, help_text='Choice Field'),
    'location': models.CharField(max_length=255, help_text='Location Field'),
}

class DynamicField(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Field Name")
    field_type = models.CharField(max_length=50, choices=[(key, key.capitalize()) for key in FIELD_TYPES.keys()])
    choices = models.TextField(blank=True, null=True, help_text="Comma-separated values for ChoiceField")
    required = models.BooleanField(default=False)
    sales_team = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dynamic_fields")

    def __str__(self):
        return self.name


### Create your models here.
# class Contact(SortableMixin):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=15)
#     message = models.TextField()
#     company = models.CharField(max_length=50, null=True, blank=True)
#     date = models.DateField(auto_now_add=True)

#     class Meta(Sortable.Meta):
#         ordering = ['the_order']

#     the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

#     def __str__(self):
#         return f"Client: {self.email}"

#     def __unicode__(self):
#         return self.date
