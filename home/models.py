from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('agent', 'Agent'),
        # ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="uploads", blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return f"{self.email} - {self.role}"

class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Client: {self.user.email}"

class AgentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agent_profile')
    agency_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Agent: {self.user.email}"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    company = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Client: {self.email}"
