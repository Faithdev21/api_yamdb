from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_username

ROLE_CHOICES = (
    ('user', 'USER',),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    role = models.CharField(
        'Role',
        choices=ROLE_CHOICES,
        default="user",
        max_length=50
    )
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        blank=False,
        null=False,
        max_length=254,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_username]
    )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff
