from decimal import Decimal

from django.db import models, transaction
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from depository.constants import (
    AMOUNT_DECIMAL_PLACES,
    AMOUNT_DECIMAL_MAX_DIGITS,
)


class OperationQuerySet(models.QuerySet):
    def report(self):
        income = Coalesce(
            Sum('amount', filter=Q(operation_type=Operation.INCOME)),
            Decimal(0),
        )
        outcome = Coalesce(
            Sum('amount', filter=Q(operation_type=Operation.OUTCOME)),
            Decimal(0),
        )
        return self.aggregate(income=income, outcome=outcome)


class OperationManager(models.Manager):
    def get_queryset(self):
        return OperationQuerySet(model=self.model, using=self._db)


class Operation(models.Model):
    """
    Operations with user Account balance
    """
    INCOME = 1
    OUTCOME = 0
    OPERATION_CHOICES = (
        (INCOME, 'Income'),
        (OUTCOME, 'Outcome'),
    )

    account = models.ForeignKey(
        to='users.Account',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Operation',
        related_name='operations',
        blank=False,
    )
    amount = models.DecimalField(
        max_digits=AMOUNT_DECIMAL_MAX_DIGITS,
        decimal_places=AMOUNT_DECIMAL_PLACES,
        null=False,
        blank=False,
    )
    operation_type = models.IntegerField(
        null=False,
        choices=OPERATION_CHOICES,
        blank=False,
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

    objects = OperationManager()

    class Meta:
        index_together = (
            ('account_id', 'operation_type'),
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.pk:
            # increment account balance
            with transaction.atomic():
                super().save(force_insert, force_update, using, update_fields)
                if self.operation_type == self.INCOME:
                    self.account.balance += self.amount
                elif self.operation_type == self.OUTCOME:
                    self.account.balance -= self.amount
                self.account.save()
        else:
            # here we should define some business logic
            # around changing operation amount or type
            super().save(force_insert, force_update, using, update_fields)
