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


class Categorie(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    rating = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
