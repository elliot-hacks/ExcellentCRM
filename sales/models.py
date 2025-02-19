from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.conf import settings
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to IPAddress
    session_id = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    page_visited = models.TextField()
    action = models.TextField(blank=True, null=True)
    visit_count = models.PositiveIntegerField(default=1)
    event_date = models.DateTimeField(default=now)
    last_visited = models.DateTimeField(default=now)  # ✅ New field


    def __str__(self):
        return f"{self.ip_address.ip_address} - {self.ip_address.country} - {self.ip_address.city} visited {self.page_visited} ({self.visit_count} times) on {self.event_date}"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.ForeignKey("IPAddress", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.contact.email} - {self.submitted_at} - {self.ip_address.ip_address if self.ip_address else 'N/A'}"


# For google calender
class GoogleCalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)
    calendar_event_id = models.CharField(max_length=255, blank=True, null=True)
    user_group = models.ForeignKey("auth.Group", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class EventResponse(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("tentative", "Tentative"),
        ("no_response", "No Response"),
    ]

    event = models.ForeignKey(GoogleCalendarEvent, on_delete=models.CASCADE, related_name="responses")
    
    # Generic Foreign Key to handle both Users and ContactMessages
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    attendee = GenericForeignKey("content_type", "object_id")

    response_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="no_response")

    def __str__(self):
        return f"{self.attendee} - {self.get_response_status_display()} ({self.event.title})"


class Analytics(models.Model):
    """Model for tracking visitor analytics based on real relations."""
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Analytics"
        verbose_name_plural = "Analytics"

    def total_users(self):
        """Count of unique users from AUTH_USER_MODEL."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.count()

    def total_emails(self):
        """Count of unique emails sent via ContactMessage."""
        from .models import ContactMessage
        return ContactMessage.objects.values('email').distinct().count()

    def total_page_visits(self):
        """Count of all page visits."""
        from .models import VisitorInfos
        return VisitorInfos.objects.count()

    def sales_contact_visits(self):
        """Count of visits to the /salescontact/ endpoint."""
        from .models import VisitorInfos
        return VisitorInfos.objects.filter(page_visited="/salescontact/").count()

    def conversion_rate(self):
        """Percentage of unique emails sent compared to users visiting /salescontact/."""
        total_emails = self.total_emails()
        sales_visits = self.sales_contact_visits()
        return (total_emails / sales_visits * 100) if sales_visits > 0 else 0

    def __str__(self):
        return "Website Analytics Data"
