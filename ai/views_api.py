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

    # Save user message to the database
    ChatMessage.objects.create(user=user, role="user", content=user_message)

    # Fetch chat history from the database
    chat_history = list(ChatMessage.objects.filter(user=user).order_by('timestamp').values('role', 'content'))

    # Add system prompt if chat history is empty
    if not chat_history:
        chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

    # Get AI response
    chat_completion = client.chat.completions.create(
        messages=chat_history + [{"role": "user", "content": user_message}],
        model="llama3-70b-8192",
        temperature=0.7,
        max_tokens=500,
    )

    ai_response = chat_completion.choices[0].message.content

    # Save assistant message to the database
    ChatMessage.objects.create(user=user, role="assistant", content=ai_response)

    return Response({"message": ai_response})

    
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_clear_chat(request):
    """API: Clears chat history for authenticated user"""
    ChatMessage.objects.filter(user=request.user).delete()
    return Response({"message": "Chat history cleared successfully"})
