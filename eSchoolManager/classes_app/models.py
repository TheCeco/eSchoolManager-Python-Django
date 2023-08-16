from django.core.exceptions import ValidationError
from django.db import models

from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.teachers_app.models import TeacherProfile


# Create your models here.
class ClassesModel(models.Model):
    CLASSES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12)
    )

    classes_choice = models.IntegerField(choices=CLASSES, unique=True)

    def __str__(self):
        return f'{self.classes_choice}'

    class Meta:
        ordering = ['id']


class TeacherClass(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    school_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('teacher', 'school_class', 'subject'), ('school_class', 'subject'),)
        ordering = ['school_class']

    def __str__(self):
        return f'{self.teacher} {self.school_class} {self.subject}'
