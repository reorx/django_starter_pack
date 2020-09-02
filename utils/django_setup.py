def setup_django(name):
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings'.format(name))
    import django
    django.setup()
