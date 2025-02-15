from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.send_mail_page, name='index'),
    path("contact/", views.contact_page, name="contact"),
    path('track-action/', views.track_action, name="track-action"),
    path("contact-success/", views.contact_success, name="contact_success"),
]
