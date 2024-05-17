import os
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True, default="123456")
    name = models.CharField(max_length=255, blank=True, null=True)
    objects = BaseUserManager()
    last_login = None
    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'user'
        ordering = ['name']
