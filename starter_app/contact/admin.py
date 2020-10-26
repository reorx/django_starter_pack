from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )
    list_display = ('id', 'email', 'company', 'created_at', 'updated_at', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id', )
        return self.readonly_fields
