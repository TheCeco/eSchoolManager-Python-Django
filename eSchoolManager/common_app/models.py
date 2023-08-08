from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from eSchoolManager.common_app.validators import NoNumInName


# Create your models here.
class SubjectsModel(models.Model):
    SUBJECT_NAME_MAX_LENGTH = 50

    subject_name = models.CharField(
        max_length=SUBJECT_NAME_MAX_LENGTH,
        blank=False,
        null=False,
        unique=True,
        validators=[
            NoNumInName()
        ]
    )

    def __str__(self):
        return self.subject_name


class GradeModel(models.Model):
    GRADE_CHOICES = (
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    )

    grade = models.IntegerField(
        choices=GRADE_CHOICES,
        validators=[
            MinValueValidator(2),
            MaxValueValidator(6)
        ],
        unique=True
    )

    def __str__(self):
        return f'{self.grade}'
