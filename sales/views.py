from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
import json


# Create your views here.
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
