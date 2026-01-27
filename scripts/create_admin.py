import os
import sys

if __name__ == '__main__':
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
    try:
        import django
        django.setup()
    except Exception as e:
        print('Failed to setup Django:', e)
        sys.exit(1)

    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.environ.get('ADMIN_USERNAME')
    email = os.environ.get('ADMIN_EMAIL', '')
    password = os.environ.get('ADMIN_PASSWORD')

    if not username or not password:
        print('ADMIN_USERNAME and ADMIN_PASSWORD environment variables must be set')
        sys.exit(2)

    try:
        if User.objects.filter(username=username).exists():
            print(f'Superuser "{username}" already exists, skipping creation')
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password)
            print(f'Superuser "{username}" created')
    except Exception as exc:
        print('Error creating superuser:', exc)
        sys.exit(3)
