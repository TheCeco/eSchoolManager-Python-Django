from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from eSchoolManager.classes_app.models import ClassesModel, TeacherClass
from eSchoolManager.teachers_app.models import TeacherProfile

UserModel = get_user_model()


class TeacherClassTest(TestCase):
    VALID_USER_DATA = {
        'email': 'teacher@abv.bg',
        'first_name': 'teacher',
        'last_name': 'teacher'
    }

    VALID_CLASS_DATA = {
        'classes_choice': 1
    }

    def test_create__when_data_is_valid__expect_to_be_created(self):
        user = UserModel.objects.create(**self.VALID_USER_DATA)
        teacher = TeacherProfile.objects.create(user=user)
        klass = ClassesModel.objects.create(**self.VALID_CLASS_DATA)
        teacher_klass = TeacherClass.objects.create(teacher=teacher, school_class=klass)
        self.assertIsNotNone(teacher_klass)

    def test_create__when_teacher_and_class_exist__expect_to_raise(self):
        user = UserModel.objects.create(**self.VALID_USER_DATA)
        teacher = TeacherProfile.objects.create(user=user)
        klass = ClassesModel.objects.create(**self.VALID_CLASS_DATA)
        TeacherClass.objects.create(teacher=teacher, school_class=klass)

        with self.assertRaises(IntegrityError):
            teacher_klass = TeacherClass.objects.create(teacher=teacher, school_class=klass)
            teacher_klass.full_clean()
