from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from eSchoolManager.accounts_app.models import SchoolUser
from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.principal_app import validators
from eSchoolManager.students_app.models import ClassesModel
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


# Create your models here.
class PrincipalProfile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    user = models.OneToOneField(SchoolUser, models.CASCADE)

    image_url = models.URLField(
        blank=True,
        null=True,
        default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRb7b5Uk6-fslFsGiTi_zqcNqdn9QqIC8AMxw&usqp=CAU'
    )

    gender = models.CharField(
        choices=GENDER,
        default=None,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        validators=[
            validators.MaxYearRange()
        ]
    )

    phone = models.CharField(
        validators=(
            validators.CheckIfValidPhone(),
            validators.NoCharInNumber()
        ),
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=75,
        blank=True,
        null=True
    )


class TeacherSubjects(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'subject')

    def validate_unique(self, exclude=None):
        qs = TeacherSubjects.objects.filter(teacher=self.teacher, subject=self.subject)
        if qs.exists():
            raise ValidationError('This teacher is already associated with this subject.')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.teacher} - {self.subject.subject_name}'
