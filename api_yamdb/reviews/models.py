from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name
