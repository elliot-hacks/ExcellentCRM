from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, FormTemplate, FormResponse, FormField
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm, DynamicForm
import json


# Create your views here.
@csrf_exempt
def save_form(request):
    if request.method == "POST":
        form_name = "Custom Form"  # You can allow users to name the form
        form = FormTemplate.objects.create(name=form_name)

        labels = request.POST.getlist("labels[]")
        types = request.POST.getlist("types[]")
        choices = request.POST.getlist("choices[]")

        for label, field_type, choice in zip(labels, types, choices):
            FormField.objects.create(
                form=form,
                label=label,
                field_type=field_type,
                choices=choice if field_type == "choice" else None
            )

        return JsonResponse({"success": True})

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


def assign_form(request):
    """Assign a form template to a contact."""
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        form_id = request.POST.get("form_id")

        if contact_form.is_valid():
            email = contact_form.cleaned_data["email"]
            contact, _ = Contact.objects.get_or_create(email=email, defaults={'name': contact_form.cleaned_data.get("name", "")})
            form = FormTemplate.objects.get(id=form_id)
            return redirect("fill_form", contact_id=contact.id, form_id=form.id)

    else:
        contact_form = ContactForm()
        forms = FormTemplate.objects.all()

    return render(request, "assign_form.html", {"contact_form": contact_form, "forms": forms})


def fill_form(request, contact_id, form_id):
    """Render and save the dynamic form assigned to the contact."""
    contact = get_object_or_404(Contact, id=contact_id)
    form_template = get_object_or_404(FormTemplate, id=form_id)
    form_fields = FormField.objects.filter(form=form_template)

    field_schema = {}
    for field in form_fields:
        field_schema[field.label] = {
            "type": field.field_type,
            "required": field.required,
            "label": field.label,
            "choices": field.choices.split(",") if field.field_type == "choice" else None
        }

    form = DynamicForm(field_schema, request.POST or None)

    if request.method == "POST" and form.is_valid():
        FormResponse.objects.create(
            contact=contact,
            form=form_template,
            response_data=form.cleaned_data
        )
        return redirect("contact_page", contact_id=contact.id)

    return render(request, "fill_form.html", {"form": form, "contact": contact, "form_template": form_template})


def render_contact_form(request, form_id):
    form_template = FormTemplate.objects.prefetch_related("fields").get(id=form_id)
    return render(request, "contact_form.html", {"form_template": form_template})
