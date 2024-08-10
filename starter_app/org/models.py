from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.db import models
from django.db.models import BooleanField, CharField, IntegerField, JSONField, TextField
from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.dispatch import receiver

from ..base.models import DatetimeMixin, PublicIdMixin
from ..consts.permission import Permission


class Org(PublicIdMixin, DatetimeMixin):
    name = CharField(max_length=64, unique=True)
    type = IntegerField(default=0)  # 0: normal; 1: regulator
    is_active = BooleanField(default=True)
    description = TextField(default='', blank=True)

    class Meta:
        db_table = 'org'

    def is_regulator_type(self):
        return self.type == 1

    def __str__(self):
        return f'id={self.id} name={self.name}'

    def __repr__(self):
        return f'<Org: {self.name}>'


codename_validator = ASCIIUsernameValidator()


class Group(PublicIdMixin, DatetimeMixin):
    org = models.ForeignKey(Org, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    permissions = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'group'
        unique_together = [['org', 'name']]

    def __str__(self):
        return f'id={self.id} name={self.name}'


username_validator = UnicodeUsernameValidator()

default_groups: list[Group] = [
    Group(
        name='管理员',
        permissions=Permission.values(),
    ),
]


@receiver(post_save, sender=Org)
def create_default_org_groups(sender, instance, created, **kwargs):
    if created:
        with atomic():
            for group in default_groups:
                Group.objects.create(org=instance, name=group.name, permissions=group.permissions)


class User(PublicIdMixin, DatetimeMixin):
    org = models.ForeignKey(Org, on_delete=models.DO_NOTHING)
    # NOTE for user registered from wechat, username is None
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
    )
    password_hash = models.CharField(max_length=128)

    # profile:
    email = CharField(max_length=64, null=True)
    display_name = models.CharField(max_length=64, null=True)
    phone = models.CharField(max_length=32, null=True)
    inviter = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

    # status:
    is_active = BooleanField()
    # has all permissions without being a member of admin group, which is the group that has all permissions
    is_superuser = models.BooleanField()

    # group and permission
    # A user will get all permissions granted to each of their groups.
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="members",  # groupA.user_set.all()
        related_query_name="user",  # Group.objects.filter(user=userA)
    )

    # last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'id={self.id} username={self.username} display_name={self.display_name}'

    def set_password(self, password):
        self.password_hash = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password_hash)

    def get_permissions(self):
        perms_set = set()
        if self.is_superuser:
            perms_set = set(Permission.keys())
        else:
            for group in self.get_groups():
                perms_set.update(group.permissions or [])
        return list(perms_set)

    def get_groups(self):
        return self.groups.all()
