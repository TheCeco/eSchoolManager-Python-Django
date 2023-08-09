from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from eSchoolManager.principal_app.models import TeacherSubjects
from eSchoolManager.common_app.models import SubjectsModel
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


class TeacherSubjectsTest(TestCase):
    VALID_USER_DATA = {
        'email': 'teacher@teacher.com',
        'first_name': 'Teacher',
        'last_name': 'Teacher'
    }

    VALID_SUBJECT_DATA = {
        'subject_name': 'Maths'
    }

    def get_data(self):
        user = UserModel.objects.create(**self.VALID_USER_DATA)
        return TeacherProfile.objects.create(user=user), SubjectsModel.objects.create(**self.VALID_SUBJECT_DATA)

    def test_create__when_data_valid__expect_to_be_crated(self):
        teacher, subject = self.get_data()
        teacher_subject = TeacherSubjects.objects.create(teacher=teacher, subject=subject)
        self.assertIsNotNone(teacher_subject)

    def test_create__when_teacher_cannot_have_same_subject__expect_to_raise(self):
        teacher, subject = self.get_data()
        TeacherSubjects.objects.create(teacher=teacher, subject=subject)

        with self.assertRaises(ValidationError):
            teacher_subject = TeacherSubjects.objects.create(teacher=teacher, subject=subject)
            teacher_subject.full_clean()
