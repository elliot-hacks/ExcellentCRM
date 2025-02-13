from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='/'),
    path('register/', views.u_register, name='u_register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
