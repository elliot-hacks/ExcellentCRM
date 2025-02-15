from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.http import JsonResponse
from .processor import log_user_action
from django.db.models import Count
import json


# Create your views here.
def track_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            log_user_action(request, data.get("action", "Unknown Action"))
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


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
            contact_message = form.save()

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
