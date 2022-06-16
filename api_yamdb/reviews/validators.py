import re
from datetime import date

from django.core.exceptions import ValidationError


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
    # '^[\w.@+-]+\z') как в ТЗ не работает
    if not re.compile(r'^[\w.@+-]+').match(name):
        raise ValidationError(
            'Можно использовать только буквы, цифры и "@.+-_".')
