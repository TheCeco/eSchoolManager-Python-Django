from django.contrib import admin

from eSchoolManager.accounts_app.models import SchoolUser


# Register your models here.
@admin.register(SchoolUser)
class SchoolUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
