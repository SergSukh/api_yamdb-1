from django.db import models
from django.contrib.auth.models import AbstractUser

from composition.models import Titles, Author

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

roles = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    password = models.CharField(max_length=50, blank=True, null=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    role = models.CharField(choices=roles, max_length=9, default='user')
    bio = models.TextField('Биография', max_length=256)
    confirmation_code = models.CharField('Код подтверждения', max_length=100)

    # PASSWORD_FIELD = 'email'

    def __str__(self):
        return str(self.username)


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        Author,
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
        default=0
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        self.review = f'Оценка: {self.score}/10 - {self.text}'
        return self.review[:30]


class Comment(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()
