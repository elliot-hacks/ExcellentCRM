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
        chat_history = request.session.get('chat_history', [system_prompt])

        chat_history.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="llama3-70b-8192", messages=chat_history, max_tokens=100, temperature=1.2
        )
        chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
        request.session['chat_history'] = chat_history

        return render(request, 'chatbot.html', {'chat_history': chat_history})

    chat_history = request.session.get('chat_history', [system_prompt])
    return render(request, 'chatbot.html', {'chat_history': chat_history})

def clear_chat(request):
    """Clears chat history in session for web-based users"""
    request.session['chat_history'] = []
    return HttpResponse("")
