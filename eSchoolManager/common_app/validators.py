import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible()
class NoNumInName:
    def __call__(self, value):
        if bool(re.match(r'\d+', value)):
            raise ValidationError('Name fields cannot contain nums')

    def __eq__(self, other):
        return True