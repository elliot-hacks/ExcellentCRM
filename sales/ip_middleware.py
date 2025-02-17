from .models import VisitorInfos, ContactMessage
from .utils import get_ip, get_location
import logging

logger = logging.getLogger(__name__)

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Fetch IP address and location
        ip_address = get_ip()
        location_data = get_location(ip_address)

        # Create or update VisitorInfos entry
        visitor, created = VisitorInfos.objects.get_or_create(
            ip_address=ip_address,
            session_id=request.session.session_key,
            defaults={
                "user": request.user if request.user.is_authenticated else None,
                "user_agent": request.META.get('HTTP_USER_AGENT'),
                "referrer": request.META.get('HTTP_REFERER'),
                "page_visited": request.path,
                "city": location_data.get("city"),
                "region": location_data.get("region"),
                "country": location_data.get("country"),
                "latitude": location_data.get("latitude"),
                "longitude": location_data.get("longitude"),
                "isp": location_data.get("isp"),
                "timezone": location_data.get("timezone"),
            }
        )

        if not created:
            visitor.visit_count += 1
            visitor.save()

        # Link VisitorInfos to ContactMessage if a form is submitted
        if request.method == 'POST' and request.path == '/salescontact/':  # Adjust the path as needed
            try:
                # Find the latest ContactMessage with the same IP address
                contact_message = ContactMessage.objects.filter(
                    email=request.POST.get('email'),
                    submitted_at__lte=now(),  # Ensure the message was submitted before now
                ).latest('submitted_at')

                # Link the VisitorInfos entry to the ContactMessage
                visitor.content_object = contact_message
                visitor.save()
                logger.info(f"Linked VisitorInfos {visitor.id} to ContactMessage {contact_message.id} via IP {ip_address}")
            except ContactMessage.DoesNotExist:
                logger.warning(f"No ContactMessage found for email: {request.POST.get('email')}")

        response = self.get_response(request)
        return response
