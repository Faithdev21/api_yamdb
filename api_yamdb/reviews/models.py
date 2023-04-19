from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='product'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author'
    )
    score = models.IntegerField(
        default=0,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Rating from 1 to 10!'},
        verbose_name='rating'
    )
    pub_date = models.DateTimeField(
        'publication date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique feedback'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='feedback'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author'
    )
    pub_date = models.DateTimeField(
        'publication_date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text
