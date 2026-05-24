from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors",
                    "placeholder": "Votre nom complet",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors",
                    "placeholder": "votre@email.com",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors resize-none",
                    "rows": 5,
                    "placeholder": "Décrivez votre projet ou votre demande...",
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
