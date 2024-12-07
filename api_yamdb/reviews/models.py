from django.db import models

from reviews.validators import validate_regular_exp, validate_year

MAX_LENGTH_NAME = 256
MAX_LENGTH_SLAG = 50


class Genre(models.Model):
    """Описании модели жанров."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLAG,
        verbose_name='Slug жанра',
        validators=[validate_regular_exp,],
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Описании модели категорий."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLAG,
        validators=[validate_regular_exp,],
        verbose_name='Slug категории',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Описании модели произведений, к которым пишут отзывы."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year,],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
