from django.contrib import admin, messages
from django.core.mail import send_mail
from django import forms
from django.urls import path
from django_admin_action_forms import action_with_form, AdminActionForm
from django.contrib.contenttypes.models import ContentType
from .models import ContactMessage, EmailTemplate, VisitorInfos, EmailTracking, IPAddress, GoogleCalendarEvent, EventResponse, Analytics, Contact
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncDay, TruncDate
from nonrelated_inlines.admin import NonrelatedStackedInline
from django.contrib.auth import get_user_model
# from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.gis.db import models
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils.html import format_html
import logging, json

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
logger = logging.getLogger(__name__)

@action_with_form(
    EmailTemplateChoiceForm,
    description="📧 Send Custom Email with Template",
)


def send_custom_email(modeladmin, request, queryset, data):
    cache_key = f"email_rate_limit_{request.user.id}"
    if cache.get(cache_key):
        modeladmin.message_user(request, "⚠️ Rate limit exceeded. Please try again later.", messages.WARNING)
        return

    selected_template = data["email_template"]
    recipient_emails = []

    # Collect email addresses from queryset
    for obj in queryset:
        if hasattr(obj, 'email'):  # For CustomUser and ContactMessage
            recipient_emails.append(obj.email)
        else:
            modeladmin.message_user(request, f"⚠️ Object {obj} does not have an email field.", messages.WARNING)

    if recipient_emails:
        try:
            send_mail(
                subject=selected_template.subject,
                message=selected_template.message,
                from_email="iamthetechoverload@gmail.com",
                recipient_list=recipient_emails,
                fail_silently=False,
            )

            # Create EmailTracking entries
            for obj in queryset:
                if hasattr(obj, 'email'):  # Ensure the object has an email field
                    content_type = ContentType.objects.get_for_model(obj)
                    EmailTracking.objects.create(
                        email_template=selected_template,
                        content_type=content_type,
                        object_id=obj.id,
                    )

            modeladmin.message_user(request, f"✅ Email sent to {len(recipient_emails)} recipients.", messages.SUCCESS)
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            modeladmin.message_user(request, f"⚠️ Failed to send email: {e}", messages.ERROR)
    else:
        modeladmin.message_user(request, "⚠️ No valid email addresses found.", messages.WARNING)

    cache.set(cache_key, True, timeout=60 * 1)

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
    # list_select_related = ["email"]
    search_fields = ("username", "email", "first_name", "last_name")
    list_per_page = 20
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
    list_display = ['user', 'ip_address', 'ip_address__country', 'page_visited', 'visit_count', 'event_date']
    list_filter = ("page_visited", 'ip_address__country', "ip_address__isp", "ip_address__timezone")  # Filter by IP-related fields
    search_fields = ("ip_address__ip_address", "page_visited")
    ordering = ("-event_date",)
    readonly_fields = ("ip_address", "page_visited", "event_date", "visit_count", "action")
    list_per_page = 20


    def has_submitted_contact_form(self, obj):
        return obj.content_type == ContentType.objects.get_for_model(ContactMessage) and obj.object_id is not None
    has_submitted_contact_form.boolean = True
    has_submitted_contact_form.short_description = "Submitted Contact Form"

    # For chart.js
    change_list_template = "admin/change_list_graph.html"  # ✅ Custom template

    def changelist_view(self, request, extra_context=None):
        """ Modify the changelist page to pass chart data for Chart.js visualization. """

        # ✅ Aggregate visitors per day
        daily_visits = (
            VisitorInfos.objects.annotate(date=TruncDate("event_date"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("date")
        )

        # ✅ Count visits per page
        page_visits = (
            VisitorInfos.objects.values("page_visited")
            .annotate(y=Count("id"))
            .order_by("-y")
        )

        # ✅ Count visits per referrer
        referrer_visits = (
            VisitorInfos.objects.exclude(referrer__isnull=True)
            .exclude(referrer="")
            .values("referrer")
            .annotate(y=Count("id"))
            .order_by("-y")
        )

        # ✅ Convert to JSON format
        chart_data = {
            "daily": list(daily_visits),
            "pages": list(page_visits),
            "referrers": list(referrer_visits),
        }

        extra_context = extra_context or {"chart_data": json.dumps(chart_data, cls=DjangoJSONEncoder)}

        return super().changelist_view(request, extra_context=extra_context)

# 🎯 Register ContactMessage and Contact in Admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")
    actions = [send_custom_email]

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("contact", "message", "submitted_at", "ip_address")
    search_fields = ("contact__name", "contact__email", "message")
    list_filter = ("submitted_at", "ip_address")
# 🎯 Register EmailTracking in Admin
@admin.register(EmailTracking)
class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ("recipient", "email_template", "sent_at", "opened_at", "clicked_link")
    list_filter = ("sent_at", "opened_at", "clicked_link")
    search_fields = ("recipient__email", "email_template__subject")
    list_per_page = 20


@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "city", "region", "country", "isp", "timezone")
    list_filter = ("country", "region", "city")
    search_fields = ("ip_address", "city", "region", "country", "isp")
    list_per_page = 20


@admin.register(GoogleCalendarEvent)
class GoogleCalendarEventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "meeting_link")
    search_fields = ("title", "description")
    list_filter = ("start_time",)
    list_per_page = 20

@admin.register(EventResponse)
class EventResponseAdmin(admin.ModelAdmin):
    list_display = ("event", "attendee", "response_status")
    list_filter = ("response_status",)
    search_fields = ("event__title", "attendee__username")
    list_per_page = 20


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    """Custom admin panel for website analytics with dynamic relations."""

    list_display = ("total_users_count", "total_emails_count", "total_page_visits_count", "sales_contact_visits_count", "conversion_rate_display")
    readonly_fields = ("total_users_count", "total_emails_count", "total_page_visits_count", "sales_contact_visits_count", "conversion_rate_display")

    # def has_add_permission(self, request):
    #     return False  # Prevents manual additions

    # def has_delete_permission(self, request, obj=None):
    #     return False  # Prevents deletions

    # def get_urls(self):
    #     """Add custom URL for analytics view in Django admin."""
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('analytics-report/', self.admin_site.admin_view(self.analytics_report_view), name='analytics_report'),
    #     ]
    #     return custom_urls + urls

    # def analytics_report_view(self, request):
    #     """Render the analytics dashboard inside Django admin."""
    #     analytics = Analytics.objects.first()
    #     if not analytics:
    #         analytics = Analytics.objects.create()

    #     context = {
    #         'analytics': analytics,
    #         'total_users': analytics.total_users(),
    #         'total_emails': analytics.total_emails(),
    #         'total_page_visits': analytics.total_page_visits(),
    #         'sales_contact_visits': analytics.sales_contact_visits(),
    #         'conversion_rate': analytics.conversion_rate(),
    #     }
    #     return render(request, 'admin/analytics_dashboard.html', context)

    def total_users_count(self, obj):
        return obj.total_users()
    total_users_count.short_description = "Total Users"

    def total_emails_count(self, obj):
        return obj.total_emails()
    total_emails_count.short_description = "Total Emails"

    def total_page_visits_count(self, obj):
        return obj.total_page_visits()
    total_page_visits_count.short_description = "Total Page Visits"

    def sales_contact_visits_count(self, obj):
        return obj.sales_contact_visits()
    sales_contact_visits_count.short_description = "Sales Contact Visits"

    def conversion_rate_display(self, obj):
        return f"{obj.conversion_rate():.2f}%"
    conversion_rate_display.short_description = "Conversion Rate"
