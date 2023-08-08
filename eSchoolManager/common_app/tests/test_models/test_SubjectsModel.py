from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from eSchoolManager.common_app.models import SubjectsModel


class SubjectsModelTest(TestCase):
    VALID_SUBJECT_DATA = {
        'subject_name': 'Maths'
    }

    def test_crete__when_data_is_valid__expect_to_be_created(self):
        subject = SubjectsModel.objects.create(**self.VALID_SUBJECT_DATA)
        subject.full_clean()
        self.assertIsNotNone(subject)

    def test_create__when_input_is_empty__expect_to_raise(self):
        invalid_data = {
            'subject_name': ''
        }

        with self.assertRaises(ValidationError):
            subject = SubjectsModel.objects.create(**invalid_data)
            subject.full_clean()

    def test_create__when_data_already_exist__expect_to_raise(self):
        SubjectsModel.objects.create(**self.VALID_SUBJECT_DATA)

        with self.assertRaises(IntegrityError):
            subject = SubjectsModel.objects.create(**self.VALID_SUBJECT_DATA)
            subject.full_clean()

    def test_create__when_num_in_subject_name__expect_to_raise(self):
        invalid_data = {
            'subject_name': 'Ma2ths'
        }

        with self.assertRaises(ValidationError):
            subject = SubjectsModel.objects.create(**invalid_data)
            subject.full_clean()
