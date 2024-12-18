from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, RegexValidator

from api_yamdb.settings import (
    EMAIL_ML,
    USERNAME_ML,
    USERNAME_REGEX
)


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )

    email = models.EmailField(
        'Почта',
        max_length=EMAIL_ML,
        unique=True,
        validators=[
            MaxLengthValidator(EMAIL_ML),
        ]
    )

    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=15,
        blank=True,
        null=True
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_ML,
        unique=True,
        validators=[
            MaxLengthValidator(USERNAME_ML),
            RegexValidator(USERNAME_REGEX),
            RegexValidator('me', message='Username cannot be "me"')
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin' or self.is_staff

    @property
    def is_moder(self):
        return self.role == 'moderator'
