from .import views
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView


app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.u_register, name='u_register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
]
