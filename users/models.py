from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, blank=False)
    is_email = models.BooleanField(default=False, verbose_name='is_email')
