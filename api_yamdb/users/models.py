from api import constants
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    """ Custom User model."""
    bio = models.TextField(
        'Biography',
        blank=True,
    )
    role = models.CharField(
        'Role',
        choices=constants.ROLE_CHOICES,
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
        return self.role == constants.MODERATOR

    @property
    def is_admin(self) -> bool:
        """ Check if the user is an admin."""
        return self.role == constants.ADMIN or self.is_staff
