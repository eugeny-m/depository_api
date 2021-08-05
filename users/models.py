from django.db import models
from django.contrib.auth.models import AbstractUser

from depository.constants import (
    AMOUNT_DECIMAL_PLACES,
    AMOUNT_DECIMAL_MAX_DIGITS,
)


class User(AbstractUser):
    """
    Django app base user.
    We dont have any difference with
    django.contrib.auth.models.User,
    but who knows the future..
    """
    pass


class Account(models.Model):
    BASE_ACCOUNT = 0
    ACCOUNT_CHOICES = (
        (BASE_ACCOUNT, 'Base account'),
    )
    
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        null=False,
        related_name='accounts',
    )
    balance = models.DecimalField(
        'Account balance',
        decimal_places=AMOUNT_DECIMAL_PLACES,
        default=0,
        max_digits=AMOUNT_DECIMAL_MAX_DIGITS,
    )
    account_type = models.IntegerField(
        'Account type',
        choices=ACCOUNT_CHOICES,
        default=BASE_ACCOUNT,
    )
    created = models.DateTimeField(
        'Created date',
        auto_now_add=True,
        null=False,
        editable=False,
    )
    updated = models.DateTimeField(
        'Updated date',
        auto_now=True,
        null=False,
    )

    class Meta:
        unique_together = ['user_id', 'account_type']
        verbose_name = 'Account'
