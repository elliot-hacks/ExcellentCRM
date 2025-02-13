from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserLoginForm, UserRegistrationForm


def index(request):
    return render(request, 'index.html')

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'register/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to dashboard after login


def u_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            messages.success(request, 'You have been registered')
            # login(request, user) # Allows direct login after registration
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register/client_register.html', {'form': form})

