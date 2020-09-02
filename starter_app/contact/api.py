from .models import Contact


def create(c: Contact) -> Contact:
    c.save()
    return c


def get_list(**kwargs):
    return Contact.objects.filter(**kwargs)


def get(**kwargs):
    return Contact.objects.get(**kwargs)
