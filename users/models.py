from django.db import models
from django.contrib.auth.models import AbstractUser


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
    ACCOUNT_CHOISES = (
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
        decimal_places=2,  # choose places according to the project specific
        default=0,
        max_digits=64,  # choose places according to the project specific
    )
    account_type = models.IntegerField(
        'Account type',
        choices=ACCOUNT_CHOISES,
        default=BASE_ACCOUNT,
    )

    class Meta:
        unique_together = ['user_id', 'account_type']
        verbose_name = 'Account'
