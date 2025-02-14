from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('', views.send_mail_page, name='send_mail')
]
