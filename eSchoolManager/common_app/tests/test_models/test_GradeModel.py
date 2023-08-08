from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from eSchoolManager.common_app.models import GradeModel


class GradeModelTest(TestCase):
    VALID_GRADE_DATA = {
        'grade': 6
    }

    def test_create__when_data_is_valid__expect_to_be_created(self):
        grade = GradeModel.objects.create(**self.VALID_GRADE_DATA)
        grade.full_clean()
        self.assertIsNotNone(grade)

    def test_create__when_grade_already_exist__expect_to_raise(self):
        GradeModel.objects.create(**self.VALID_GRADE_DATA)

        with self.assertRaises(IntegrityError):
            grade = GradeModel.objects.create(**self.VALID_GRADE_DATA)
            grade.full_clean()

    def test_create__when_input_is_below_minimum__expect_to_raise(self):
        invalid_data = {
            'grade': 1
        }

        with self.assertRaises(ValidationError):
            grade = GradeModel.objects.create(**invalid_data)
            grade.full_clean()

    def test_create__when_input_is_above_maximum__expect_to_raise(self):
        invalid_data = {
            'grade': 8
        }

        with self.assertRaises(ValidationError):
            grade = GradeModel.objects.create(**invalid_data)
            grade.full_clean()