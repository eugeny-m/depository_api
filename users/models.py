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
