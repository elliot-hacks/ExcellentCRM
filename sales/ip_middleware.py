from .models import VisitorInfos, IPAddress
from .utils import get_ip, get_location  # ✅ Still importing & using get_location()

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Get the actual IP address from the request
        ip_address = get_ip(request)

        # ✅ Fetch location data (without "ip" key)
        location_data = get_location(ip_address)

        # ✅ Ensure `ip_address` is an `IPAddress` instance
        ip_instance, created = IPAddress.objects.get_or_create(
            ip_address=ip_address,  # ✅ Correct field name
            defaults=location_data  # ✅ Now valid, does not contain "ip"
        )

        # ✅ Assign `ip_address` as an `IPAddress` instance, NOT a string
        visitor, created = VisitorInfos.objects.get_or_create(
            ip_address=ip_instance,  # ✅ Correct ForeignKey assignment
            session_id=request.session.session_key,
            defaults={
                "user": request.user if request.user.is_authenticated else None,
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "referrer": request.META.get("HTTP_REFERER"),
                "page_visited": request.path,
            }
        )

        if not created:
            visitor.visit_count += 1
            visitor.save(update_fields=["visit_count"])

        response = self.get_response(request)
        return response
