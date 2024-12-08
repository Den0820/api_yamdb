from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверка корректности года выпуска."""

    if value > datetime.now().year:
        raise ValidationError(
            ('Год выпуска не может быть больше текущего!'),
            params={'value': value},)


def validate_regular_exp(value):
    """Проверка на наличие только буквенно-цифровых символов."""

    if not str(value).isalnum():
        raise ValidationError(
            ('Разрешены только буквенно-цифровые символы!'),
            params={'value': value},)
