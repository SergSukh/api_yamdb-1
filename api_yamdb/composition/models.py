from django.db import models


class Author(models.Model):
    """Модель Автор для будущих расширений"""
    first_name = models.TextField()
    last_name = models.TextField()
    slug = models.SlugField(
        max_length=80,
        unique=True
    )

    def __str__(self) -> str:
        self.name = self.first_name + ' ' + self.last_name
        return self.name


class Genres(models.Model):
    """Модель жанры, мнгое кмногому"""
    genre = models.CharField(max_length=200, unique=False)

    def __str__(self):
        return self.genre


class Categories(models.Model):
    """Модель категории одно к многим """
    category = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField

    def __str__(self) -> str:
        return self.slug


class Titles(models.Model):
    """Модель Произведение, базовая модель"""
    title = models.TextField(
        'Название произведения',
        help_text='Введите название произведения'
    )
    title_urls = models.URLField(
        unique=True,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='titles',
        blank=True,
        null=True
    )
    year = models.IntegerField(
        'Год релиза',
        help_text='Введите год релиза')
    genres = models.ManyToManyField(Genres, through='GenreTitle')
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=False,
        blank=False,
        related_name='titles'
    )

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'
