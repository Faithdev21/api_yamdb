from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = [
    ('USER', 'user'),
    ('MODERATOR', 'moderator'),
    ('ADMIN', 'admin'),
]


class User(AbstractUser):
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    role = models.CharField(
        'Role',
        choices=ROLE_CHOICES,
        default='USER',
        max_length=10
    )

    def __str__(self) -> str:
        return self.username
