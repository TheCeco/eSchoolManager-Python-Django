from django.contrib import admin

from eSchoolManager.principal_app.models import TeacherSubjects
from eSchoolManager.teachers_app.models import TeacherProfile


# Register your models here.
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    