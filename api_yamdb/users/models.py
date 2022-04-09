from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):

    roles = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField('Email', unique=True)
    role = models.CharField(
        'Роль пользователя',
        choices=roles,
        max_length=9,
        default='user'
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELDS = "email"

    def __str__(self):
        return str(self.username)
