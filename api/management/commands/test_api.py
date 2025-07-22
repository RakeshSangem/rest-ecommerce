import json
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class Command(BaseCommand):
    help = 'Test API endpoints with authentication'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username to authenticate with'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='http://localhost:8000',
            help='Base URL for the API'
        )

    def handle(self, *args, **options):
        username = options['username']
        base_url = options['base_url'].rstrip('/')

        # Get user and generate token
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
            return

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        self.stdout.write(f"Testing API with user: {username}")
        self.stdout.write("-" * 50)

        # Test endpoints
        endpoints = [
            ('GET', '/products/', 'List products'),
            ('GET', '/orders/', 'List orders'),
            ('GET', '/products/info/', 'Product info'),
            ('GET', '/api/schema/', 'API schema'),
        ]

        for method, endpoint, description in endpoints:
            url = f"{base_url}{endpoint}"

            try:
                response = None
                if method == 'GET':
                    response = requests.get(url, headers=headers, timeout=10)

                if response:
                    status_color = self.style.SUCCESS if response.status_code < 400 else self.style.ERROR

                    self.stdout.write(
                        f"{method} {endpoint} - {description}: "
                        f"{status_color(str(response.status_code))}"
                    )

                    if response.status_code >= 400:
                        self.stdout.write(f"  Error: {response.text[:100]}...")

            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    f"{method} {endpoint} - {description}: "
                    f"{self.style.ERROR('Connection Error')}"
                )
                self.stdout.write(f"  Error: {str(e)}")

        self.stdout.write("-" * 50)
        self.stdout.write("Test completed!")
        self.stdout.write(f"Access token: {access_token[:20]}...")
