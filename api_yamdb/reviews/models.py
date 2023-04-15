from django.db import models


class Feedback(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='feedback',
        verbose_name='product'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedback',
        verbose_name='author'
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
                fields=('title', 'author', ),
                name='unique feedback'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
