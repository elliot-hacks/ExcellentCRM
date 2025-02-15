from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.utils.timezone import now

User = get_user_model()

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.submitted_at}"


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255, help_text="Enter the email subject.")
    message = models.TextField(help_text="Enter the email message.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


# 🎯 Model to Track Visitor Information
class VisitorInfos(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    session_id = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    page_visited = models.TextField()
    action = models.TextField(blank=True, null=True)  # Stores specific actions like "Clicked CTA"
    event_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.ip_address} visited {self.page_visited} on {self.event_date}"