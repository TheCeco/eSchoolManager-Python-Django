import datetime
import re

from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible()
class CheckIfValidPhone:
    def __call__(self, value):
        if (not value.startswith('+') or len(value) != 13) and (not value.startswith('0') or len(value) != 10):
            raise ValidationError('Phone number must starts with "0" and be 10 chars long '
                                  'or starts with "+" and be 13 chars long')

    def __eq__(self, other):
        return True


@deconstructible()
class NoCharInNumber:
    def __call__(self, value):
        if not bool(re.match(r'^(\+|0)?[0-9]+$', value)):
            raise ValidationError('The phone number cannot contain letters')

    def __eq__(self, other):
        return True


@deconstructible()
class MaxYearRange:
    MAX_YEAR = 100

    def __init__(self, max_year=MAX_YEAR):
        self.max_year = max_year

    def __call__(self, value):
        current_year = datetime.date.today().year

        if current_year - value.year > self.max_year or value.year >= current_year:
            raise ValidationError('Please enter a valid year')

    def __eq__(self, other):
        return True
