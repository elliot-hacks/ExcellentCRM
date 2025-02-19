from django.urls import path
from .views_api import api_chat_with_ai, api_clear_chat
from .views import chatbot, clear_chat

urlpatterns = [
    # Web-based views
    path("", chatbot, name="chatbot"),
    path("clear_chat/", clear_chat, name="clear_chat"),

    # API endpoints
    path("api/chat/", api_chat_with_ai, name="api_chat_with_ai"),
    path("api/clear_chat/", api_clear_chat, name="api_clear_chat"),
]
