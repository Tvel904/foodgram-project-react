from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 150
MAX_LENGTH_EMAIL = 254


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    email = models.EmailField(
        'Email пользователя',
        max_length=MAX_LENGTH_EMAIL,
        unique=True
    )
    username = models.CharField(
        'Никнейм пользователя',
        max_length=MAX_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH,
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=MAX_LENGTH,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

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
        ordering = ('author',)
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_author_subcriber'
            ),
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
