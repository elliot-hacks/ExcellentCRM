from django.contrib import admin, messages
from django.core.mail import send_mail
from django import forms
from django_admin_action_forms import action_with_form, AdminActionForm
from .models import ContactMessage, EmailTemplate, VisitorInfos
from django.contrib.auth import get_user_model

User = get_user_model()

# 🎯 Form for Selecting Email Template
class EmailTemplateChoiceForm(AdminActionForm):
    email_template = forms.ModelChoiceField(
        queryset=EmailTemplate.objects.all(),
        required=True,
        label="Select Email Template",
    )

    class Meta:
        list_objects = True  # Show the list of selected users
        help_text = "Choose an email template to send to the selected users."

# 🎯 Function to Send Emails with Selected Template
@action_with_form(
    EmailTemplateChoiceForm,
    description="📧 Send Custom Email with Template",
)
def send_custom_email(modeladmin, request, queryset, data):
    selected_template = data["email_template"]
    recipient_emails = [user.email for user in queryset if user.email]

    if recipient_emails:
        send_mail(
            subject=selected_template.subject,
            message=selected_template.message,
            from_email="iamthetechoverload@gmail.com",
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        modeladmin.message_user(request, f"✅ Email sent to {len(recipient_emails)} recipients.", messages.SUCCESS)
    else:
        modeladmin.message_user(request, "⚠️ No valid email addresses found.", messages.WARNING)

# 🎯 Register EmailTemplate in Admin
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_at")
    search_fields = ("subject",)

# 🎯 Register Users with Actions
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active", "user_groups")
    list_filter = ("is_active", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    actions = [send_custom_email]  # Add the custom email action

    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    user_groups.short_description = "Groups"

# 🎯 Register Contact Messages
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "submitted_at")
    search_fields = ("name", "email", "message")
    actions = [send_custom_email]  # Add the custom email action


# Track VIsitors
@admin.register(VisitorInfos)
class VisitorInfosAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "page_visited", "event_date")
    list_filter = ("event_date",)
    search_fields = ("ip_address", "page_visited")