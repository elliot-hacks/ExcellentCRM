from .import views
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='/'),
    path('register/', views.u_register, name='u_register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    re_path(r'^activate/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$', views.activate, name='activate'),
]
