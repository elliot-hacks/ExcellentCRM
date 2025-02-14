from django.contrib import admin
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import ContactMessage
from django.contrib.auth import get_user_model


User = get_user_model()
# Action to send emails to selected users
def send_bulk_email(modeladmin, request, queryset):
    recipient_emails = [user.email for user in queryset if user.email]

    if recipient_emails:
        send_mail(
            subject="Sales Notification",
            message="Hello, this is an important message from our Sales Team.",
            from_email="thisguyhack@gmail.com",
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        messages.success(request, f"Email sent successfully to {len(recipient_emails)} recipients.")
    else:
        messages.error(request, "No valid email addresses found.")

send_bulk_email.short_description = "Send Email to Selected Users"

# Admin Model for Users with Email Sending
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


# Function to send custom emails
def send_custom_email(modeladmin, request, queryset):
    try:
        latest_email = EmailTemplate.objects.latest("created_at")  # Get latest email template
    except EmailTemplate.DoesNotExist:
        messages.error(request, "No email templates available. Create one first.")
        return
    
    recipient_emails = [user.email for user in queryset if user.email]

    if recipient_emails:
        send_mail(
            subject=latest_email.subject,
            message=latest_email.message,
            from_email="iamthetechoverload.com",
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        messages.success(request, f"Email sent to {len(recipient_emails)} users.")
    else:
        messages.error(request, "No valid email addresses found.")

send_custom_email.short_description = "Send Custom Email to Selected Users"

# Register Email Template in Admin
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_at")
    search_fields = ("subject",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active", "user_groups") 
    list_filter = ("is_active", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    actions = [send_bulk_email]

    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    user_groups.short_description = "Groups"


# Admin Model for Contact Comments
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "submitted_at")
    search_fields = ("name", "email", "message")
    actions = [send_bulk_email, send_custom_email]


