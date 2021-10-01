from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """
    Класс пользователей
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer.' +
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    email = models.EmailField(
        'почта',
        unique=True,
        max_length=254,
        blank=False,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    password = models.CharField('пароль', max_length=150, blank=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    """
    Класс для подписочной модели.
    """
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name='подписчик'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'], name='unique_subscriber'
            ),
        ]
