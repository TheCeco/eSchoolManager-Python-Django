from django.contrib import admin

from eSchoolManager.students_app.models import AddGradeToStudentModel, StudentProfile


# Register your models here.
@admin.register(AddGradeToStudentModel)
class AddGradeToStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'grade']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['school_class']
