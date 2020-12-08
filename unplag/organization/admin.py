from django.contrib import admin
from .models import Organization

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)
    list_display = ('name', 'title', 'date_created', 'unique_code')

admin.site.register(Organization, OrganizationAdmin)
