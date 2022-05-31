from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширяет пользовательскую модель полями bio и role"""
    ROLES = [
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    email = models.EmailField
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(max_length=20, choices=ROLES)
