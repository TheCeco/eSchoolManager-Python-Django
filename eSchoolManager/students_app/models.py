from django.contrib.auth import get_user_model
from django.db import models

from eSchoolManager.accounts_app.models import SchoolUser
from eSchoolManager.classes_app.models import ClassesModel
from eSchoolManager.common_app.models import SubjectsModel, GradeModel
from eSchoolManager.students_app.validators import CheckIfValidPhone, CheckIfValidLength

UserModel = get_user_model()


# Create your models here.
class StudentProfile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, blank=True, null=True)

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
        null=True
    )

    phone = models.CharField(
        validators=(
            CheckIfValidPhone(),
            CheckIfValidLength()
        ),
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    school_class = models.ForeignKey(ClassesModel, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.email})'


class AddGradeToStudentModel(models.Model):
    grade = models.ForeignKey(GradeModel, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectsModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['student_id', 'subject_id']
