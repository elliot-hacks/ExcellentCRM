from django.db import models

class Contact(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email


class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class FormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text Field'),
        ('email', 'Email Field'),
        ('phone', 'Phone Number'),
        ('checkbox', 'Checkbox'),
        ('date', 'Date Field'),
        ('choice', 'Dropdown'),
    ]

    form = models.ForeignKey(FormTemplate, on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    choices = models.TextField(blank=True, null=True, help_text="Comma-separated values for dropdowns")
    required = models.BooleanField(default=True)


class FormResponse(models.Model):
    """Stores user responses per assigned form"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="responses")
    form = models.ForeignKey(FormTemplate, on_delete=models.CASCADE, related_name="responses")
    response_data = models.JSONField(default=dict)  # Stores actual form values
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact.email} - {self.form.name}"
