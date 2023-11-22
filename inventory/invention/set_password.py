from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Set password for a user'

    def add_arguments(self, parser):
        parser.add_argument('rollno', type=str, help='Username of the user')
        parser.add_argument('password', type=str, help='New password for the user')

    def handle(self, *args, **options):
        rollno = options['rollno']
        password = options['password']

        try:
            user = User.objects.get(rollno=rollno)
            user.password = make_password(password)
            user.save()

            self.stdout.write(self.style.SUCCESS(f"Password set successfully for user {rollno}"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{rollno}' not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
