from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from eSchoolManager.classes_app.models import ClassesModel


class ClassesModelTest(TestCase):
    VALID_CLASS_DATA = {
        'classes_choice': 1
    }

    def test_create__when_class_is_valid__expect_to_be_created(self):
        klas = ClassesModel.objects.create(**self.VALID_CLASS_DATA)
        klas.full_clean()
        self.assertIsNotNone(klas)

    def test_create__when_class_is_invalid__expect_to_be_created(self):
        invalid_data = {
            'classes_choice': 13
        }

        with self.assertRaises(ValidationError):
            klas = ClassesModel.objects.create(**invalid_data)
            klas.full_clean()

    def test_create_when_class_exist__expect_to_raise(self):
        ClassesModel.objects.create(**self.VALID_CLASS_DATA)

        with self.assertRaises(IntegrityError):
            klas = ClassesModel.objects.create(**self.VALID_CLASS_DATA)
            klas.full_clean()
