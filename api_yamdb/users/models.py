from api import constants
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

ROLE_CHOICES: tuple[tuple[str, str], tuple[str, str], tuple[str, str]] = (
    ('user', 'USER',),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN'),
)


class User(AbstractUser):
    """ Custom User model."""
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    role = models.CharField(
        'Role',
        choices=ROLE_CHOICES,
        default="user",
        max_length=constants.USER_ROLE_MAX_LENGTH
    )
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        blank=False,
        null=False,
        max_length=constants.USER_EMAIL_MAX_LENGTH,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=constants.USER_USERNAME_MAX_LENGTH,
        blank=False,
        null=False,
        unique=True,
        validators=[validate_username]
    )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self) -> bool:
        """ Check if the user is a moderator."""
        return self.role == 'moderator'

    @property
    def is_admin(self) -> bool:
        """ Check if the user is an admin."""
        return self.role == 'admin' or self.is_staff
