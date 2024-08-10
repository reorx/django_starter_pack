from django.contrib import admin

from .models import LogicUnit


@admin.register(LogicUnit)
class LogicUnitAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )
    list_display = ('id', 'name', 'created_at', 'updated_at', )
    update_fields = ['name', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id', )
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.save(update_fields=self.update_fields)
