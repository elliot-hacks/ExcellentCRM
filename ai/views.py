from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from groq import Groq
from .models import ChatMessage
import os


API_KEY = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=API_KEY)

system_prompt = {"role": "system", "content": "You are a helpful assistant. You reply with very short answers."}

@login_required
def chatbot(request):
    """Handles chatbot web-based interaction"""
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Save user message to the database
        ChatMessage.objects.create(user=request.user, role="user", content=user_input)

        # Fetch chat history from the database
        chat_history = list(ChatMessage.objects.filter(user=request.user).order_by('timestamp').values('role', 'content'))

        # Add system prompt if chat history is empty
        if not chat_history:
            chat_history = [system_prompt]

        # Get AI response
        response = client.chat.completions.create(
            model="llama3-70b-8192", messages=chat_history, max_tokens=100, temperature=1.2
        )
        ai_response = response.choices[0].message.content

        # Save assistant message to the database
        ChatMessage.objects.create(user=request.user, role="assistant", content=ai_response)

        # Append AI response to chat history
        chat_history.append({"role": "assistant", "content": ai_response})

        return render(request, 'chatbot.html', {'chat_history': chat_history})

    # Fetch chat history from the database for GET requests
    chat_history = list(ChatMessage.objects.filter(user=request.user).order_by('timestamp').values('role', 'content'))
    if not chat_history:
        chat_history = [system_prompt]

    return render(request, 'chatbot.html', {'chat_history': chat_history})

def clear_chat(request):
    """Clears chat history in session and database for web-based users"""
    # Clear session chat history
    request.session['chat_history'] = []

    # Clear database chat history for the current user
    ChatMessage.objects.filter(user=request.user).delete()

    return HttpResponse("Chat history cleared successfully")

