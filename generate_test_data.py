import argparse
import os
import uuid
import random

from decimal import Decimal

# setup django before models import
import django
from django.db.models import DateField, DateTimeField
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'depository.settings')
django.setup()

from users.models import Account, User
from operations.models import Operation
from django.utils import timezone
from datetime import timedelta


def get_parser():
    parser = argparse.ArgumentParser(description='Generate test users data')
    parser.add_argument(
        '--users_count',
        type=int,
        default=20000,
        help='How many users to create'
    )
    parser.add_argument(
        '--operations_count',
        type=int,
        default=10,
        help='How many operations per account to create'
    )
    return parser


def monkey_patch_autonow(model):
    for field in model._meta.get_fields():
        if isinstance(field, (DateTimeField, DateField)):
            field.auto_now = False
            field.auto_now_add = False


def generate_test_data(users_count, operations_count):
    # Just to set Operation.create/update date
    monkey_patch_autonow(Operation)

    # generate users
    users_to_create = []
    for i in range(users_count):
        user = User(username=uuid.uuid4().hex)
        users_to_create.append(user)
    User.objects.bulk_create(users_to_create, batch_size=1000)
    user_ids = [u[0] for u in User.objects.values_list('id')]
    
    # generate accounts
    accounts_to_create = []
    for user_id in user_ids:
        accounts_to_create.append(Account(user_id=user_id))
    Account.objects.bulk_create(accounts_to_create, batch_size=1000)
    accounts = list(Account.objects.all())
    
    # generate operations
    operation_types = tuple(
        choice[0] for choice
        in Operation.OPERATION_CHOICES
    )
    now = timezone.localtime()
    operations_to_create = []
    for account in accounts:
        for i in range(operations_count):
            operation_type = random.choice(operation_types)
            amount = Decimal(random.randint(0, 1000000), ) / 100
            created = now - timedelta(days=random.randint(0, 365))
            operation = Operation(
                amount=amount,
                account_id=account.id,
                operation_type=operation_type,
                created=created,
                updated=created,
            )
            operation.created = created
            operations_to_create.append(operation)
            if operation_type == Operation.INCOME:
                account.balance += amount
            elif operation_type == Operation.OUTCOME:
                account.balance -= amount
    Operation.objects.bulk_create(operations_to_create, batch_size=1000)
    
    # update Account balances
    # bulk_create doesn't call Operation.save method,
    # so we should handle balance manually
    Account.objects.bulk_update(accounts, ['balance'])
    print(f'{User.objects.count()} with operations created!')


if __name__ == '__main__':
    
    parser = get_parser()
    args = parser.parse_args()
    
    generate_test_data(
        users_count=args.users_count,
        operations_count=args.operations_count
    )
