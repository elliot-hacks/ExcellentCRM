from .import views
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.u_register, name='u_register'),
    path('login/', views.u_login, name="login"),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
