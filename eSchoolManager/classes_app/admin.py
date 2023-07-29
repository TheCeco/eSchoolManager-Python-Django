from django.contrib import admin

from eSchoolManager.classes_app.models import TeacherClass, ClassesModel


# Register your models here.
@admin.register(ClassesModel)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['classes_choice']


@admin.register(TeacherClass)
class TeacherClassAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'school_class']
