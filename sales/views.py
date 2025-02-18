from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage, IPAddress, EmailTracking
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.conf import settings
from .forms import ContactForm
from .processor import log_user_action
import json
from .utils import get_ip
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Create your views here.
# Calender views
def google_calender_init(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_API_SCOPES,
        redirect_uri=settings.REDIRECT_URI,
    )
    authorization_uri, state = flow.authorization_url(
        access_type='offline',
        include_granted_scope='true'
    )
    request.session['state'] = state
    return redirect(authorization_uri)


def google_calender_redirect(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_API_SCOPES,
        state = state,
        redirect_uri=settings.REDIRECT_URI,
    )

    flow.fetch_token(authorization_response = request.build_absolute_uri())
    credentials = flow.credentials

    request.session['credentials'] = credentials_to_dict(credentials)
    return HttpResponse('Calender intergration complete')


def credentials_to_dict(credentials):
    return{
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_url,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }


# Email views
def track_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            log_user_action(request, data.get("action", "Unknown Action"))
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def email_open_tracking(request, tracking_id):
    """ Tracks email opens using a 1x1 transparent image """
    tracking = get_object_or_404(EmailTracking, id=tracking_id)

    # Mark the email as opened (if not already)
    if not tracking.opened_at:
        tracking.opened_at = now()
        tracking.save(update_fields=["opened_at"])

    # Return a 1x1 transparent pixel
    pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xc0\xc0\xc0\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return HttpResponse(pixel_data, content_type="image/gif")


def email_link_tracking(request, tracking_id, redirect_url):
    """ Tracks email link clicks before redirecting """
    tracking = get_object_or_404(EmailTracking, id=tracking_id)

    tracking.mark_clicked()
    return redirect(redirect_url)


def get_visitor_statistics():
    unique_visitors = VisitorInfos.objects.values('ip_address').distinct().count()
    most_visited_pages = VisitorInfos.objects.values('page_visited').annotate(count=Count('page_visited')).order_by('-count')[:5]
    top_referrers = VisitorInfos.objects.values('referrer').annotate(count=Count('referrer')).order_by('-count')[:5]

    return {
        "unique_visitors": unique_visitors,
        "most_visited_pages": most_visited_pages,
        "top_referrers": top_referrers,
    }

# Mailing
def send_mail_page(request):
    context = {}

    if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
    
    return render(request, "send_mail.html", context)


def contact_page(request):
    """Render the contact form and handle submissions."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data and link to IPAddress
            contact_message = form.save(commit=False)
            ip_address = get_ip(request)

            # Retrieve or create IPAddress instance
            ip_instance, created = IPAddress.objects.get_or_create(ip_address=ip_address)
            contact_message.ip_address = ip_instance  # Link to IPAddress instance
            contact_message.save()

            # Send notification email
            subject = "New Contact Form Submission"
            message = f"A new comment was submitted by {contact_message.email}:\n\n{contact_message.message}"
            recipient_email = "iamthetechoverload@gmail.com"

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )

            return redirect("sales:contact_success")

    else:
        form = ContactForm()

    return render(request, "sales/contact.html", {"form": form})
def contact_success(request):
    """Render the success page after a user submits a contact form."""
    return render(request, "sales/contact_success.html")
