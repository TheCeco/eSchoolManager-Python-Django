from django.contrib import admin

from eSchoolManager.students_app.models import AddGradeToStudentModel


# Register your models here.
@admin.register(AddGradeToStudentModel)
class AddGradeToStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'grade']
