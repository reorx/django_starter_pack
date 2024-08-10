from django.contrib import admin
from django.db.models.expressions import F
from django import forms
from .models import Org, Group, User
from ..base.admin import BaseModelAdmin


class OrgMixin:
    @admin.display(description='Org Name', ordering='org')
    def get_org_name(self, obj):
        # return obj.org.name
        return obj._org_name
    # get_org_name.admin_order_field = 'org'
    # get_org_name.short_description = 'Org Name'

    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related('book')
    def get_queryset(self, request):
        # https://stackoverflow.com/a/69360403/596206
        # to make this work, OrgMixin must be put in front of BaseModelAdmin in the inheritance list
        return super().get_queryset(request).annotate(
            _org_name = F('org__name')
        )


@admin.register(Org)
class OrgAdmin(BaseModelAdmin):
    readonly_fields = ('pid', 'created_at', 'updated_at', )
    list_display = ('pid', 'name', 'type', 'is_active', 'created_at', 'updated_at', )


@admin.register(Group)
class GroupAdmin(OrgMixin, BaseModelAdmin):
    readonly_fields = ('pid', 'created_at', 'updated_at', )
    list_display = ('pid', 'name', 'get_org_name', 'created_at', 'updated_at', )
    list_filter = ('org__name', )


class UserForm(forms.ModelForm):
    def clean(self):
        # use .get incase user selects nothing, 'org is required' is checked after this method
        org = self.cleaned_data.get('org')
        groups = self.cleaned_data.get('groups')
        if org and groups:
            for group in groups:
                if group.org != org:
                    raise forms.ValidationError('Group must belong to the same org as the user')


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ('pid', 'created_at', 'updated_at', 'password_hash')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(OrgMixin, BaseModelAdmin):
    form = UserForm

    readonly_fields = ('pid', 'created_at', 'updated_at', 'password_hash')
    list_display = ('pid', 'username', 'get_org_name', 'is_active', 'is_superuser', 'created_at', 'updated_at', )
    list_filter = ('org__name', )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            # already excluded in UserCreateForm.Meta.exclude, return empty tuple to avoid overwriting
            return tuple()
        return self.readonly_fields

    # https://django-tricks.github.io/Custom-Admin-Add-Form/
    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """
        if obj is None:
            kwargs['form'] = UserCreateForm
        return super().get_form(request, obj, **kwargs)
