from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

UserModel = get_user_model()


class SchoolUserTest(TestCase):
    VALID_USER_DATA = {
        'email': 'rapidfire114@gmail.com',
        'first_name': 'Tsvetan',
        'last_name': 'Minchev',
        'password': 'lowwol123',
    }

    def test_create__when_all_the_data_is_valid___expect_to_be_created(self):
        user = UserModel.objects.create(**self.VALID_USER_DATA)
        user.full_clean()
        self.assertIsNotNone(user.pk)

    def test_create__when_non_latin_letters__expect_to_be_created(self):
        self.VALID_USER_DATA = {
            **self.VALID_USER_DATA,
            'first_name': 'Цветан'
        }

        user = UserModel.objects.create(**self.VALID_USER_DATA)
        user.full_clean()
        self.assertIsNotNone(user.pk)

    def test_create__when_non_latin_letters_and_number__expect_to_raise(self):
        self.VALID_USER_DATA = {
            **self.VALID_USER_DATA,
            'first_name': 'Цветан1'
        }

        with self.assertRaises(ValidationError):
            user = UserModel.objects.create(**self.VALID_USER_DATA)
            user.full_clean()

    def test_create__when_number_in_first_name__expect_to_raise(self):
        invalid_data = {
            **self.VALID_USER_DATA,
            'first_name': 'Tsvetan1'
        }

        with self.assertRaises(ValidationError):
            user = UserModel.objects.create(
                **invalid_data
            )
            user.full_clean()

    def test_create__when_first_name_is_empty__expect_to_raise(self):
        invalid_data = {
            **self.VALID_USER_DATA,
            'first_name': ''
        }

        with self.assertRaises(ValidationError):
            user = UserModel.objects.create(
                **invalid_data
            )
            user.full_clean()

    def test_create__when_number_in_last_name__expect_to_raise(self):
        invalid_data = {
            **self.VALID_USER_DATA,
            'last_name': 'Minchev123'
        }

        with self.assertRaises(ValidationError):
            user = UserModel.objects.create(
                **invalid_data
            )
            user.full_clean()

    def test_create__when_last_name_is_None__expect_to_raise(self):
        invalid_data = {
            **self.VALID_USER_DATA,
            'last_name': ''
        }

        with self.assertRaises(ValidationError):
            user = UserModel.objects.create(
                **invalid_data
            )
            user.full_clean()

    def test_create__when_email_exist__expect_to_raise(self):
        UserModel.objects.create(**self.VALID_USER_DATA)

        with self.assertRaises(IntegrityError):
            user = UserModel.objects.create(**self.VALID_USER_DATA)
            user.full_clean()
