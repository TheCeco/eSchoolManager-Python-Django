from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible()
class CheckIfValidPhone:
    def __call__(self, value):
        if not value.startswith('+') and not value.startswith('0'):
            raise ValidationError('Phone number must starts with + or 0')

    def __eq__(self, other):
        return True


@deconstructible()
class CheckIfValidLength:
    def __call__(self, value):
        if len(value) != 10 and len(value) != 13:
            raise ValidationError('Length of phone number is not correct')

    def __eq__(self, other):
        return True
