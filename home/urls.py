from .import views
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.u_register, name='u_register'),
    path('login/', views.u_login, name="login"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
]
# 0oopsD@y$