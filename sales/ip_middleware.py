from .models import VisitorInfos, IPAddress
from .utils import get_ip, get_location
from django.utils.timezone import now


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Fetch visitor IP address
        ip_address = get_ip(request)

        # ✅ Fetch or create IP record
        location_data = get_location(ip_address)
        ip_instance, created = IPAddress.objects.get_or_create(
            ip_address=ip_address,
            defaults=location_data
        )

        # ✅ Track visitor info
        visitor, created = VisitorInfos.objects.get_or_create(
            ip_address=ip_instance,
            session_id=request.session.session_key,
            defaults={
                "user": request.user if request.user.is_authenticated else None,
                "user_agent": request.META.get('HTTP_USER_AGENT'),
                "referrer": request.META.get('HTTP_REFERER'),
                "page_visited": request.path,
            }
        )

        if not created:
            visitor.visit_count += 1
            visitor.last_visited = now()
            visitor.save(update_fields=["visit_count", "last_visited"])

        response = self.get_response(request)
        return response
