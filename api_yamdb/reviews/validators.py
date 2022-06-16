import re
from datetime import date

from django.core.exceptions import ValidationError

REGEX_FOR_USERNAME = re.compile(r'^[\w.@+-]+')


def validate_year(value):
    year = date.today().year
    if not (value <= year):
        raise ValidationError(
            'Год выпуска произведения не должен быть в будущем! '
            f'Вы ввели: {value}'
        )
    return value


def validate_username(name):
    if name == 'me':
        raise ValidationError('Имя пользователя "me" использовать нельзя!')
    if not REGEX_FOR_USERNAME.fullmatch(name):
        raise ValidationError(
            'Можно использовать только буквы, цифры и "@.+-_".')
