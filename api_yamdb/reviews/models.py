from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)

from users.models import User


class Author(models.Model):
    """ Модель Автор для будущих расширений. """
    first_name = models.TextField()
    last_name = models.TextField()
    slug = models.SlugField(
        max_length=80,
        unique=True
    )

    def __str__(self) -> str:
        self.name = f'{self.first_name} {self.last_name}'
        return self.name


class Genres(models.Model):
    """Модель жанры, многое к многому"""
    name = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Categories(models.Model):
    """Модель категории одно к многим """
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.CharField(
        null=True,
        max_length=3000,
        verbose_name='Описание'
    )

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    """Модель Произведение, базовая модель"""

    name = models.TextField()
    title_urls = models.URLField(
        unique=True,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='titles',
        blank=True,
        null=True
    )
    year = models.IntegerField(
        'Год релиза',
        help_text='Введите год релиза'
    )
    genre = models.ManyToManyField(Genres, through='GenreTitle')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=True,
        blank=True,
        related_name='titles'
    )
    description = models.CharField(
        null=True,
        max_length=3000,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_followers")
        ]

    def __str__(self):
        self.review = 'Автор: {}, текст: {} оценка'.format(
            self.author, self.text)
        return self.review


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()

    def __str__(self):
        return self.author
