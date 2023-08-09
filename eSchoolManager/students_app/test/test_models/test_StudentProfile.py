import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from eSchoolManager.students_app.models import StudentProfile

UserModel = get_user_model()


class StudentProfileTest(TestCase):
    VALID_USER_DATA = {
        'email': 'student@student.com',
        'first_name': 'Student',
        'last_name': 'Student'
    }

    VALID_STUDENT_DATA = {
        'date_of_birth': '2001-09-09',
        'phone': '0895316715'
    }

    def get_user(self):
        return UserModel.objects.create(**self.VALID_USER_DATA)

    def test_create__when_data_valid_and_phone_number_starts_with_0_and_10_chars_long__expect_to_be_created(self):
        student = StudentProfile.objects.create(**self.VALID_STUDENT_DATA, user=self.get_user())
        student.full_clean()
        self.assertIsNotNone(student)

    def test_create__when_data_valid_and_phone_number_starts_with_plus_and_13_chars_long__expect_to_be_created(self):
        self.VALID_STUDENT_DATA = {
            **self.VALID_STUDENT_DATA,
            'phone': '+359895316715'
        }

        student = StudentProfile.objects.create(**self.VALID_STUDENT_DATA, user=self.get_user())
        student.full_clean()
        self.assertIsNotNone(student)

    def test_create__when_date_is_below_minimum__expect_to_raise(self):
        invalid_data = {
            **self.VALID_STUDENT_DATA,
            'date_of_birth': str(datetime.date.today().year - StudentProfile.MAX_YEAR_RANGE - 1) + '-09-09'
        }

        with self.assertRaises(ValidationError):
            student = StudentProfile.objects.create(**invalid_data, user=self.get_user())
            student.full_clean()

    def test_create__when_date_is_above_last_year__expect_to_raise(self):
        invalid_data = {
            **self.VALID_STUDENT_DATA,
            'date_of_birth': str(datetime.date.today().year) + '-09-09'
        }

        with self.assertRaises(ValidationError):
            student = StudentProfile.objects.create(**invalid_data, user=self.get_user())
            student.full_clean()

    def test_create__when_phone_number_is_not_valid__expect_to_raise(self):
        invalid_data = {
            **self.VALID_STUDENT_DATA,
            'phone': '12345678'
        }

        with self.assertRaises(ValidationError):
            student = StudentProfile.objects.create(**invalid_data, user=self.get_user())
            student.full_clean()

    def test_create__when_char_in_phone_number__expect_to_raise(self):
        invalid_data = {
            **self.VALID_STUDENT_DATA,
            'phone': '0234567894f'
        }

        with self.assertRaises(ValidationError):
            student = StudentProfile.objects.create(**invalid_data, user=self.get_user())
            student.full_clean()
