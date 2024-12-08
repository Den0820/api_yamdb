from django.db import models
from django.contrib.auth import get_user_model
from reviews.validators import MinValueValidator, MaxValueValidator, validate_regular_exp, validate_year

MAX_LENGTH_NAME = 256
MAX_LENGTH_SLAG = 50

User  = get_user_model()

class Genre(models.Model):
    """Описание модели жанров."""

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
    """Описание модели категорий."""

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
    """Описание модели произведений, к которым пишут отзывы."""

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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review'),
        ]
        ordering = ['-pub_date']


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author} - {self.review.title} - {self.text[:20]}'
