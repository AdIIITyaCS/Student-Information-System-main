#!/usr/bin/env python3
"""
Sync student documents from MongoDB collection into Django's SQLite DB.
Run this once on the server after migrations to populate StudentProfile entries
from existing Mongo documents so admin CRUD becomes available.
"""
import os
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
    try:
        import django
        django.setup()
    except Exception as e:
        print('Failed to setup Django:', e)
        sys.exit(1)

    from django.contrib.auth import get_user_model
    from main.mongo import get_mongo_collection
    from main.models import StudentProfile

    User = get_user_model()

    collection = get_mongo_collection()
    if collection is None:
        print('Mongo collection not available. Check MONGO_URI and env vars.')
        return

    for doc in collection.find():
        roll = str(doc.get('roll_number', '')).strip()
        first = doc.get('first_name', '') or ''
        last = doc.get('last_name', '') or ''
        email = doc.get('email', '') or ''

        if not roll:
            # skip docs without roll number
            print('Skipping doc without roll:', doc.get('_id'))
            continue

        # Skip if profile with same roll exists
        if StudentProfile.objects.filter(roll_number=roll).exists():
            print('Profile exists for roll', roll)
            continue

        # Decide username
        username = roll
        if User.objects.filter(username=username).exists():
            username = f'mongo_{roll}'
            # ensure uniqueness
            i = 1
            while User.objects.filter(username=username).exists():
                username = f'mongo_{roll}_{i}'
                i += 1

        password = User.objects.make_random_password()
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first, last_name=last)

        profile = StudentProfile.objects.create(
            user=user,
            roll_number=roll,
            course=doc.get('course'),
            profile_completed=doc.get('profile_completed', False),
        )
        print('Created user/profile for roll', roll)


if __name__ == '__main__':
    main()
