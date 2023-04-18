from django.db import models
from django.contrib.auth.models import AbstractUser


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.DateTimeField(
        'Created date', auto_now_add=True
    )
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Category',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        verbose_name='Genre',
        blank=True,
    )

    def __str__(self):
        return self.name
