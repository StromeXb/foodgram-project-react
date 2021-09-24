from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    User class
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=254,
        blank=False,
        error_messages={
             'unique': _("A user with that email already exists."),
        },
    )
    password = models.CharField(_('password'), max_length=150, blank=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']


class Subscribe(models.Model):
    """
    Класс для подписочной модели.
    """
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author"
    )

    class Meta:
        unique_together = [["subscriber", "author"]]
