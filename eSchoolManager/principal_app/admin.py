from django.contrib import admin

from eSchoolManager.principal_app.models import PrincipalProfile, TeacherSubjects


# Register your models here.
@admin.register(PrincipalProfile)
class PrincipalProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(TeacherSubjects)
class TeacherSubjectsAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject']
    list_filter = ['subject']


