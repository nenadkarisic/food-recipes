import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from recipes.models import User


class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'

    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true', dest='no_input')
        parser.add_argument('--username', type=str)
        parser.add_argument('--email', type=str)
        parser.add_argument('--first_name', type=str)
        parser.add_argument('--last_name', type=str)

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} was created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} with email {email} already exists.'))
