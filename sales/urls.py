from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.send_mail_page, name='send_mail'),
    path("contact/", views.contact_page, name="contact"),
    path("contact-success/", views.contact_success, name="contact_success"),
]
