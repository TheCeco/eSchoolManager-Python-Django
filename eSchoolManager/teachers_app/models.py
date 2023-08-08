from django.contrib.auth import get_user_model
from django.db import models

from eSchoolManager.accounts_app.models import SchoolUser
from eSchoolManager.common_app.models import GradeModel, SubjectsModel
from eSchoolManager.teachers_app import validators

UserModel = get_user_model()


# Create your models here.
class TeacherProfile(models.Model):
    MIN_YEAR_RANGE = 100

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE)

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
            validators.MaxYearRange(MIN_YEAR_RANGE)
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

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.email})'
