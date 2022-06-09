from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    year = date.today().year
    if not (value <= year):
        raise ValidationError('Проверьте год выпуска!')
    return value
