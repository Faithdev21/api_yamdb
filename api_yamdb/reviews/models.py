from api import constants
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class GenreCategory(models.Model):
    """Base class for Genre and Category."""
    name = models.CharField(max_length=constants.NAME_MAX_LENGTH)
    slug = models.SlugField(
        max_length=constants.SLUG_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Genre(GenreCategory):
    """Genres of titles."""

    class Meta:
        verbose_name: str = 'genre'
        verbose_name_plural: str = 'genre'


class Category(GenreCategory):
    """Categories of titles."""

    class Meta:
        verbose_name: str = 'category'
        verbose_name_plural: str = 'category'


class Title(models.Model):
    """Titles."""
    name = models.CharField(
        max_length=constants.TITLE_NAME_MAX_LENGTH, unique=True)
    year = models.IntegerField(null=True, blank=True)
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
        through="GenreTitle",
        related_name='title',
        verbose_name='Genre',
        blank=False,
    )

    class Meta:
        verbose_name: str = 'title'
        verbose_name_plural: str = 'title'
        ordering: tuple[str] = ('year',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Linking table for genres and categories."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genre_title',
        verbose_name='Genre',
        blank=True, null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_title',
        verbose_name='Title',
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'


class Review(models.Model):
    """Reviews of titles."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='product'
    )
    text = models.CharField(
        max_length=constants.REVIEW_TEXT_MAX_LENGTH
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author'
    )
    score = models.IntegerField(
        default=1,
        validators=(
            MinValueValidator(constants.MIN_SCORE_AMOUNT),
            MaxValueValidator(constants.MAX_SCORE_AMOUNT)
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
        verbose_name: str = 'review'
        verbose_name_plural: str = 'review'
        constraints: list[UniqueConstraint] = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique review'
            )]
        ordering: tuple[str] = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Comments of titles."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='feedback'
    )
    text = models.CharField(
        max_length=constants.COMMENT_TEXT_MAX_LENGTH
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
        verbose_name: str = 'comment'
        verbose_name_plural: str = 'comments'
        ordering: tuple[str] = ('-pub_date',)

    def __str__(self):
        return self.text
