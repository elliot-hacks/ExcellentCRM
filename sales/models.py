from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.submitted_at}"


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255, help_text="Enter the email subject.")
    message = models.TextField(help_text="Enter the email message.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
