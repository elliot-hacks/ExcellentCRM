from django.utils.timezone import now  # ✅ Use timezone-aware function
from django.conf import settings
from .models import VisitorInfos, IPAddress
from .utils import get_ip, get_location
import socket
import datetime


def save_visitor_infos(request):
    """Tracks page visits and updates visit counts."""
    if not hasattr(request, 'META'):
        print("🚨 Error: Invalid request object")
        return {}

    try:
        ip_address = get_ip(request)  # ✅ Get visitor's IP

        # ✅ Ensure IP exists in the database
        ip_instance, _ = IPAddress.objects.get_or_create(ip_address=ip_address)

        # ✅ Track page visit
        page_visited = request.path
        present_date = now()

        visit_entry, created = VisitorInfos.objects.get_or_create(
            ip_address=ip_instance,
            page_visited=page_visited,
            defaults={"last_visited": present_date, "visit_count": 1}
        )

        if not created:
            visit_entry.visit_count += 1
            visit_entry.last_visited = present_date
            visit_entry.save()

    except Exception as e:
        print(f"🚨 Error saving visitor info: {e}")

    return {}


def log_user_action(request, action):
    """Logs user actions such as clicks, form submissions, etc."""
    if not hasattr(request, 'META'):
        print("Error: Request object is not valid.")
        return
    
    try:
        ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
        session_id = request.session.session_key
        user = request.user if request.user.is_authenticated else None

        VisitorInfos.objects.create(
            user=user,
            ip_address=ip,
            session_id=session_id,
            page_visited=request.path,
            action=action,
            event_date=now()  # ✅ Fix naive datetime error
        )
    except Exception as e:
        print(f"Error saving visitor info: {e}")
