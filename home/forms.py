from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, ClientProfile, AgentProfile


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'username', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'
        if commit:
            user.save()
            ClientProfile.objects.create(user=user, full_name=self.cleaned_data['full_name'], phone=self.cleaned_data['phone'])
        return user

