import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from groq import Groq
from .models import ChatMessage

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_chat_with_ai(request):
    """API: Handles chatbot interactions"""
    user = request.user
    user_message = request.data.get("message")

    if not user_message:
        return Response({"error": "Message is required"}, status=400)

    ChatMessage.objects.create(user=user, role="user", content=user_message)

    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": user_message}],
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=100
    )

    ai_response = chat_completion.choices[0].message.content
    ChatMessage.objects.create(user=user, role="assistant", content=ai_response)

    return Response({"message": ai_response})

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_clear_chat(request):
    """API: Clears chat history for authenticated user"""
    ChatMessage.objects.filter(user=request.user).delete()
    return Response({"message": "Chat history cleared successfully"})
