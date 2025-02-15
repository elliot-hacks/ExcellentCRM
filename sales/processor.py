from django.utils.timezone import now  # ✅ Use timezone-aware function
from django.conf import settings
from .models import VisitorInfos
import socket
import datetime

def save_visitor_infos(request):
    """ Context processor for tracking visitors. """
    context_nb_visitors = 0

    if not hasattr(request, 'META'):
        print("Error: Invalid request object")
        return {}  # ✅ Return an empty dictionary if request is invalid

    try:
        # Get visitor IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Check if IP address is valid
        try:
            socket.inet_aton(ip)
            ip_valid = True
        except socket.error:
            ip_valid = False

        if ip_valid:
            present_date = now()  # ✅ Use timezone-aware datetime
            ref_date_1 = present_date - datetime.timedelta(days=1)

            # Save visitor info only if not already recorded in the last 24 hours
            if not VisitorInfos.objects.filter(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1).exists():
                VisitorInfos.objects.create(
                    ip_address=ip,
                    page_visited=request.path,
                    event_date=present_date
                )
            else:
                visitor_infos_obj = VisitorInfos.objects.get(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1)
                visitor_infos_obj.event_date = present_date
                visitor_infos_obj.save()

    except Exception as e:
        print(f"Error saving visitor info: {e}")

    # Retrieve the number of active visitors in the last 5 minutes
    ref_date = now() - datetime.timedelta(minutes=5)  # ✅ Use timezone-aware datetime
    context_nb_visitors = VisitorInfos.objects.filter(event_date__gte=ref_date).values_list('ip_address', flat=True).distinct().count()

    return {"context_nb_visitors": context_nb_visitors}  # ✅ Ensure a dictionary is returned



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
