from django import forms
from .models import DynamicField

def generate_dynamic_form():
    class SalesForm(forms.Form):
        for field in DynamicField.objects.all():
            field_name = field.name.lower().replace(" ", "_")
            if field.field_type == 'text':
                locals()[field_name] = forms.CharField(widget=forms.Textarea, required=field.required)
            elif field.field_type == 'char':
                locals()[field_name] = forms.CharField(required=field.required)
            elif field.field_type == 'email':
                locals()[field_name] = forms.EmailField(required=field.required)
            elif field.field_type == 'phone':
                locals()[field_name] = forms.CharField(max_length=15, required=field.required)
            elif field.field_type == 'date':
                locals()[field_name] = forms.DateField(widget=forms.SelectDateWidget, required=field.required)
            elif field.field_type == 'datetime':
                locals()[field_name] = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=field.required)
            elif field.field_type == 'checkbox':
                locals()[field_name] = forms.BooleanField(required=field.required)
            elif field.field_type == 'location':
                locals()[field_name] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter location'}), required=field.required)
            elif field.field_type == 'choices':
                choices_list = [(choice.strip(), choice.strip()) for choice in field.choices.split(",") if choice.strip()]
                locals()[field_name] = forms.ChoiceField(choices=choices_list, required=field.required)
    return SalesForm
