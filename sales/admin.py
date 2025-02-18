from django.contrib import admin, messages
from django.core.mail import send_mail
from django import forms
from django_admin_action_forms import action_with_form, AdminActionForm
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils.html import format_html
import logging
from .models import (
    ContactMessage, EmailTemplate, VisitorInfos, EmailTracking, IPAddress
)
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

# 🎯 Form for Selecting Email Template
class EmailTemplateChoiceForm(AdminActionForm):
    email_template = forms.ModelChoiceField(
        queryset=EmailTemplate.objects.all(),
        required=True,
        label="Select Email Template",
    )

    class Meta:
        list_objects = True  # Show list of selected users
        help_text = "Choose an email template to send to the selected users."

# 🎯 Function to Send Emails with Rate Limiting
@action_with_form(
    EmailTemplateChoiceForm,
    description="📧 Send Custom Email with Template",
)

def send_custom_email(modeladmin, request, queryset, data):
    selected_template = data["email_template"]
    recipient_emails = []

    for obj in queryset:
        if hasattr(obj, 'email'):
            recipient_emails.append(obj.email)

    if recipient_emails:
        for obj in queryset:
            if hasattr(obj, 'email'):
                content_type = ContentType.objects.get_for_model(obj)
                tracking = EmailTracking.objects.create(
                    email_template=selected_template,
                    content_type=content_type,
                    object_id=obj.id,
                )

                # Replace links in email message
                message_with_tracking = selected_template.message.replace(
                    "https://yourdestination.com/",
                    f"https://yourdomain.com/track-click/{tracking.id}/?redirect_url=https://yourdestination.com/"
                )

                send_mail(
                    subject=selected_template.subject,
                    message="HTML version required",
                    from_email="your-email@example.com",
                    recipient_list=[obj.email],
                    fail_silently=False,
                    html_message=message_with_tracking,  # ✅ Sends email with tracked links
                )

# 🎯 Contact Form Submission Filter for Admin
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
    list_per_page = 20
    actions = [send_custom_email]

    def user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    user_groups.short_description = "Groups"

# 🎯 Register VisitorInfos in Admin with Geo-Data
@admin.register(VisitorInfos)
class VisitorInfosAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address", "get_city", "get_region", "get_country",
        "page_visited", "visit_count", "event_date",
        "has_submitted_contact_form", "get_timezone", "get_isp",
    )
    list_filter = ("page_visited", "ip_address__country", "ip_address__region", "ip_address__city")
    search_fields = ("ip_address__ip_address", "ip_address__city", "ip_address__region", "ip_address__country", "page_visited")
    ordering = ("-event_date",)
    readonly_fields = ("ip_address", "page_visited", "event_date", "visit_count", "action")

    def has_submitted_contact_form(self, obj):
        return obj.content_type == ContentType.objects.get_for_model(ContactMessage) and obj.object_id is not None
    has_submitted_contact_form.boolean = True
    has_submitted_contact_form.short_description = "Submitted Contact Form"

    def get_city(self, obj):
        return obj.ip_address.city if obj.ip_address else "-"
    get_city.short_description = "City"

    def get_region(self, obj):
        return obj.ip_address.region if obj.ip_address else "-"
    get_region.short_description = "Region"

    def get_country(self, obj):
        return obj.ip_address.country if obj.ip_address else "-"
    get_country.short_description = "Country"

    def get_timezone(self, obj):
        return obj.ip_address.timezone if obj.ip_address else "-"
    get_timezone.short_description = "Timezone"

    def get_isp(self, obj):
        return obj.ip_address.isp if obj.ip_address else "-"
    get_isp.short_description = "ISP"

# 🎯 Register ContactMessage in Admin
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message", "submitted_at", "get_ip_address")
    search_fields = ("name", "email", "message")
    list_per_page = 20
    actions = [send_custom_email]

    def get_ip_address(self, obj):
        return obj.ip_address.ip_address if obj.ip_address else "N/A"
    get_ip_address.short_description = "IP Address"

# 🎯 Register EmailTracking in Admin
@admin.register(EmailTracking)
class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ("recipient", "email_template", "sent_at", "opened_at", "clicked_link")
    list_filter = ("sent_at", "opened_at", "clicked_link")
    search_fields = ("recipient__email", "email_template__subject")
    list_per_page = 20
