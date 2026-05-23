from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Lamarana Diallo"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "lamaranamamadousdiallo@gmail.com"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Racontez votre projet, vos besoins ou une collaboration souhaitée",
                }
            ),
        }
        labels = {
            "name": "Nom complet",
            "email": "Email",
            "message": "Message",
        }
        error_messages = {
            "name": {"required": "Un nom est requis."},
            "email": {"required": "Un email est requis.", "invalid": "L'email semble incorrect."},
            "message": {"required": "Écrivez un message pour détailler votre demande."},
        }
