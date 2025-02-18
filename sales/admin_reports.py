from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from .models import VisitorInfos, ContactMessage, EmailTracking

@staff_member_required  # Restrict access to Admins only
def analytics_dashboard(request):
    """ Renders analytics dashboard in Django Admin with Chart.js """

    # Visitor Analytics
    total_visitors = VisitorInfos.objects.values("ip_address").distinct().count()
    most_visited_pages = VisitorInfos.objects.values("page_visited").annotate(count=Count("page_visited")).order_by("-count")[:5]
    top_referrers = VisitorInfos.objects.values("referrer").annotate(count=Count("referrer")).order_by("-count")[:5]
    
    # Contact Form Analytics
    total_submissions = ContactMessage.objects.count()
    submission_rate = (total_submissions / total_visitors * 100) if total_visitors else 0

    # Email Analytics
    total_sent_emails = EmailTracking.objects.count()
    opened_emails = EmailTracking.objects.filter(opened_at__isnull=False).count()
    clicked_links = EmailTracking.objects.filter(clicked_link=True).count()
    
    email_open_rate = (opened_emails / total_sent_emails * 100) if total_sent_emails else 0
    email_click_rate = (clicked_links / total_sent_emails * 100) if total_sent_emails else 0

    context = {
        "total_visitors": total_visitors,
        "most_visited_pages": most_visited_pages,
        "top_referrers": top_referrers,
        "total_submissions": total_submissions,
        "submission_rate": round(submission_rate, 2),
        "total_sent_emails": total_sent_emails,
        "opened_emails": opened_emails,
        "clicked_links": clicked_links,
        "email_open_rate": round(email_open_rate, 2),
        "email_click_rate": round(email_click_rate, 2),
    }
    
    return render(request, "admin/analytics_dashboard.html", context)

# Register the new URL in Django Admin
def get_admin_urls(urls):
    custom_urls = [
        path("analytics-dashboard/", analytics_dashboard, name="analytics_dashboard"),
    ]
    return custom_urls + urls
