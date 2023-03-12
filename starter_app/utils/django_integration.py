import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starter_app.settings')


def setup_starter_app():
    django.setup()

    # ensure ORM is usable
    from django.contrib.auth.models import User

    count = User.objects.count()
    print(f'* dwtoolkit integration successful, users count: {count}')
