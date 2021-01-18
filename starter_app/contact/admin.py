from django.contrib import admin
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    # name = forms.CharField(widget=CustomWidget())

    class Meta:
        model = Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )
    list_display = ('id', 'email', 'company', 'created_at', 'updated_at', )
    form = ContactForm
    update_fields = ['email', 'company', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id', )
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.save(update_fields=self.update_fields)
