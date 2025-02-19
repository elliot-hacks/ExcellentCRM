from django.contrib import admin
from django.urls import path, include
# from sales.admin_reports import analytics_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    # path('accounts/', include('allauth.socialaccount.urls')),
    path('', include('home.urls')),
    path('ai', include('ai.urls')),
    path('sales', include('sales.urls')),
    path("admin/action-forms/", include("django_admin_action_forms.urls")),
    # path("admin/analytics-dashboard/", analytics_dashboard, name="analytics_dashboard"),
]


admin.site.site_header = "Excellent Stuff"
admin.site.site_title = "Excellent Admin"
admin.site.index_title = "Karibu Excellent Guidelines"
