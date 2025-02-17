from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

User = get_user_model()

# 🎯 Contact Form Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    # Generic relation to VisitorInfos
    visitor_info = GenericRelation('VisitorInfos', related_query_name='contact_messages')

    def __str__(self):
        return f"{self.email} - {self.submitted_at}"

    class Meta:
        verbose_name = "ContactMessage"
        verbose_name_plural = "ContactMessages"

# 🎯 Email Template Model
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
    email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    
    # Generic ForeignKey for recipient
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    recipient = GenericForeignKey('content_type', 'object_id')

    sent_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_link = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient} - {self.email_template.subject}"


# 🎯 Model to Track Visitor Information with Generic Relations
class VisitorInfos(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    session_id = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    page_visited = models.TextField()
    action = models.TextField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=1)
    event_date = models.DateTimeField(default=now)

    # Location fields
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # ISP and Timezone fields
    isp = models.CharField(max_length=255, blank=True, null=True)  # Add ISP
    timezone = models.CharField(max_length=255, blank=True, null=True)  # Add timezone

    # Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.ip_address} visited {self.page_visited} ({self.visit_count} times) on {self.event_date}"

    class Meta:
        verbose_name = "VisitorInfo"
        verbose_name_plural = "VisitorInfos"
        # unique_together = ('user', 'session_id')
