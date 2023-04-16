from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = [
    ('USER', 'user'),
    ('MODERATOR', 'moderator'),
    ('ADMIN', 'admin'),
]


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True,
        null=False,
    ),
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    role = models.CharField(
        'Role',
        choices=ROLE_CHOICES,
        default='USER'
    )

    def __str__(self) -> str:
        return self.username
