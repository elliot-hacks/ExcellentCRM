from django.contrib import admin, messages
from django.core.mail import send_mail
from django import forms
from django_admin_action_forms import action_with_form, AdminActionForm
from django.contrib.contenttypes.models import ContentType
from .models import ContactMessage, EmailTemplate, VisitorInfos
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils.html import format_html

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

# 🎯 Admin Filter to Link VisitorInfos and ContactMessage
class ContactMessageFilter(admin.SimpleListFilter):
    title = "Sales Contact Form Submissions"
    parameter_name = "salescontact_submission"

    def lookups(self, request, model_admin):
        """ Define filter options with submission percentage """
        total_visitors = VisitorInfos.objects.filter(page_visited="/salescontact/").count()
        total_submitted = VisitorInfos.objects.filter(
            page_visited="/salescontact/",
            content_type=ContentType.objects.get_for_model(ContactMessage),
            object_id__isnull=False
        ).count()

        submission_percentage = (total_submitted / total_visitors * 100) if total_visitors else 0

        return [
            ("submitted", f"Submitted Contact Form ({total_submitted}/{total_visitors}, {submission_percentage:.2f}%)"),
            ("not_submitted", f"Did Not Submit ({total_visitors - total_submitted}/{total_visitors})"),
        ]

    def queryset(self, request, queryset):
        """ Filter VisitorInfos based on ContactMessage submissions for /salescontact/ """
        content_type = ContentType.objects.get_for_model(ContactMessage)
        sales_contact_visits = queryset.filter(page_visited="/salescontact/")

        if self.value() == "submitted":
            return sales_contact_visits.filter(content_type=content_type, object_id__isnull=False)
        elif self.value() == "not_submitted":
            return sales_contact_visits.filter(Q(content_type__isnull=True) | Q(object_id__isnull=True))
        
        return sales_contact_visits

# 🎯 Register VisitorInfos in Admin
@admin.register(VisitorInfos)
class VisitorInfosAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "page_visited", "visit_count", "event_date", "action", "has_submitted_contact_form")
    list_filter = ("page_visited", ContactMessageFilter)  # Add custom filter
    search_fields = ("ip_address", "page_visited")
    ordering = ("-event_date",)
    readonly_fields = ("ip_address", "page_visited", "event_date", "visit_count", "action")  

    def has_submitted_contact_form(self, obj):
        """ Check if the visitor submitted a ContactMessage form """
        return obj.content_type == ContentType.objects.get_for_model(ContactMessage) and obj.object_id is not None
    has_submitted_contact_form.boolean = True
    has_submitted_contact_form.short_description = "Submitted Contact Form"

# 🎯 Register ContactMessage in Admin
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "submitted_at")
    search_fields = ("name", "email", "message")
    actions = [send_custom_email]
