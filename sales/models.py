from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

User = get_user_model()

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255, help_text="Enter the email subject.")
    message = models.TextField(help_text="Enter the email message.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def clean(self):
        if not self.subject or not self.message:
            raise ValidationError("Subject and message are required.")

    class Meta:
        verbose_name = "EmailTemplate"
        verbose_name_plural = "EmailTemplates"


class EmailTracking(models.Model):
    email_template = models.ForeignKey("EmailTemplate", on_delete=models.CASCADE)
    
    # Generic ForeignKey for recipient
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    recipient = GenericForeignKey("content_type", "object_id")

    sent_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True, blank=True)  # ✅ Stores when email was opened
    clicked_link = models.BooleanField(default=False)
    click_count = models.PositiveIntegerField(default=0)

    def mark_opened(self):
        """ Mark email as opened """
        if not self.opened_at:
            self.opened_at = now()
            self.save(update_fields=["opened_at"])

    def __str__(self):
        return f"{self.recipient} - {self.email_template.subject}"

# 🎯 Model to Track Visitor Information with Generic Relations
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)  # Ensure IP addresses are unique
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    isp = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.ip_address

class VisitorInfos(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to IPAddress
    session_id = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    page_visited = models.TextField()
    action = models.TextField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=1)
    event_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.ip_address} visited {self.page_visited} ({self.visit_count} times) on {self.event_date}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to IPAddress

    def __str__(self):
        return f"{self.email} - {self.submitted_at} - {self.ip_address.ip_address}"