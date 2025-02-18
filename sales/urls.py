from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.send_mail_page, name='index'),
    path("contact/", views.contact_page, name="contact"),
    path('track-action/', views.track_action, name="track-action"),
    path("contact-success/", views.contact_success, name="contact_success"),
    path('track-email/<int:tracking_id>/', views.email_open_tracking, name="email_open_tracking"),
    path('track-click/<int:tracking_id>/', views.email_link_tracking, name="email_link_tracking"),
]
