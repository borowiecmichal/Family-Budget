from django.db import models

from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

