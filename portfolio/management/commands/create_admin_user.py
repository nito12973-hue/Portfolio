import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crée un superutilisateur si aucun n\'existe'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')
        
        if not password:
            self.stdout.write(
                self.style.ERROR('DJANGO_ADMIN_PASSWORD non défini. Le superutilisateur ne sera pas créé.')
            )
            return
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Le superutilisateur "{username}" existe déjà.')
            )
            return
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Superutilisateur "{username}" créé avec succès.')
        )
