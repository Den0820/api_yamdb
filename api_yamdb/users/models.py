from django.contrib.auth.models import AbstractUser
from django.db import models


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
        unique=True
    )

    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=15,
        blank=True,
        null=True
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
        return self.is_superuser or self.role == "admin" or self.is_staff

    @property
    def is_moder(self):
        return self.role == 'moderator'
