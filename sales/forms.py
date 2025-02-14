from django import forms
import json
from .models import Contact, FormTemplate, FormResponse

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'name']

class DynamicForm(forms.Form):
    """Creates form fields dynamically based on field_schema"""

    def __init__(self, field_schema, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field_props in field_schema.items():
            field_type = field_props.get("type", "text")
            required = field_props.get("required", False)
            label = field_props.get("label", field_name)

            if field_type == "text":
                self.fields[field_name] = forms.CharField(label=label, required=required)
            elif field_type == "email":
                self.fields[field_name] = forms.EmailField(label=label, required=required)
            elif field_type == "phone":
                self.fields[field_name] = forms.CharField(label=label, required=required)
            elif field_type == "checkbox":
                self.fields[field_name] = forms.BooleanField(label=label, required=required)
            elif field_type == "date":
                self.fields[field_name] = forms.DateField(label=label, required=required)
            elif field_type == "choice":
                choices = field_props.get("choices", [])
                self.fields[field_name] = forms.ChoiceField(choices=[(c, c) for c in choices], label=label, required=required)
