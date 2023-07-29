from django.contrib import admin

from .models import SubjectsModel, GradeModel


# Register your models here.
@admin.register(SubjectsModel)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['subject_name']


@admin.register(GradeModel)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade']