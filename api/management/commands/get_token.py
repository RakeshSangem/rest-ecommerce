import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate JWT tokens for a user (for local testing)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to generate token for',
            required=True
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'headers', 'curl'],
            default='json',
            help='Output format (json, headers, or curl)'
        )

    def handle(self, *args, **options):
        username = options['username']
        output_format = options['format']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
            return

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        if output_format == 'json':
            tokens = {
                'user_id': user.id,
                'username': user.username,
                'access': access_token,
                'refresh': refresh_token,
                'expires_in': '1 hour'
            }
            self.stdout.write(json.dumps(tokens, indent=2))

        elif output_format == 'headers':
            self.stdout.write("Add this header to your requests:")
            self.stdout.write(f"Authorization: Bearer {access_token}")

        elif output_format == 'curl':
            self.stdout.write("Example curl command:")
            self.stdout.write(
                f'curl -H "Authorization: Bearer {access_token}" '
                f'http://localhost:8000/orders/'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Tokens generated successfully for user: {username}')
        )
