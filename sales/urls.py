from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.send_mail_page, name='send_mail'),
    path("assign-form/", views.assign_form, name="assign_form"),
    path("fill-form/<int:contact_id>/<int:form_id>/", views.fill_form, name="fill_form"),
    path("save-form/", views.save_form, name="save_form"),  # Missing in your original URLs
    path("render-form/<int:form_id>/", views.render_contact_form, name="render_contact_form"),  # Allows rendering specific form
]
