from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribers', verbose_name='Автор рецепта')
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscribe', verbose_name='Подписчик')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_author_subcriber'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
