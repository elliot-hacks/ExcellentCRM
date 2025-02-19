from django import forms
from .models import Contact, ContactMessage

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = ContactMessage
        fields = ["message"]  # Only include fields from ContactMessage

    def save(self, commit=True):
        """Override save method to create or get Contact and associate with ContactMessage."""
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")
        message = self.cleaned_data.get("message")

        # Create or get a Contact instance
        contact, _ = Contact.objects.get_or_create(email=email, defaults={"name": name, "phone": phone})
        
        # Create a ContactMessage instance linked to the Contact
        contact_message = ContactMessage(contact=contact, message=message)

        if commit:
            contact_message.save()

        return contact_message
