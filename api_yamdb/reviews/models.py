from django.db import models


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.DateTimeField(
        'Created date', auto_now_add=True
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Category',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Genre',
    )

    def __str__(self):
        return self.name
    