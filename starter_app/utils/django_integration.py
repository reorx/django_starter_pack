import os

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starter_app.settings')


def setup_django(check_models=False):
    django.setup()

    # ensure ORM is usable
    if check_models:
        from django.contrib.auth.models import User

        count = User.objects.count()
        print(f'* starter_app django integration successful, users count: {count}')
