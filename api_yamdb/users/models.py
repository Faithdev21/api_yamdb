from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


ROLE_CHOICES = (
    ('USER', 'user'),
    ('MODERATOR', 'moderator'),
    ('ADMIN', 'admin'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    username = models.CharField(
        'Логин',
        unique=True,
        null=False,
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[\w.@+-]+\z',
                message='Incorrect name'
            )
        ]
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        null=False,
    ),
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    ),
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    ),
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        choices=ROLE_CHOICES,
        default='USER'
    )

    def __str__(self) -> str:
        return self.username
