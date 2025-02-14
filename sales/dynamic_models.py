from django.db import models
from .models import DynamicField, FIELD_TYPES

def generate_sales_model():
    fields = {
        'id': models.AutoField(primary_key=True),
        'created_at': models.DateTimeField(auto_now_add=True),
    }

    for field in DynamicField.objects.all():
        field_name = field.name.lower().replace(" ", "_")
        if field.field_type == 'choices':
            choices_list = [(choice.strip(), choice.strip()) for choice in field.choices.split(",") if choice.strip()]
            fields[field_name] = models.CharField(max_length=255, choices=choices_list, blank=not field.required)
        else:
            fields[field_name] = FIELD_TYPES[field.field_type]

    return type('SalesData', (models.Model,), fields)

SalesData = generate_sales_model()
