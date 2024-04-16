import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
from public.utils.file import generate_filtered_file_list


class User(AbstractBaseUser):
    ROLES = (
        ("Student", "Student"),
        ("Admin", "Admin"),
        ("Principle", "Principle"),
        ("Coach", "Coach"),
    )
    GENDERS = (
        (1, "Male"),
        (0, "Female"),
    )
    code = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.CharField(max_length=30, unique=True, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True, default="123456")
    role = models.CharField(max_length=20, choices=ROLES, blank=True, null=True, default="Student")
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.SmallIntegerField(choices=GENDERS, blank=True, null=True)
    DOB = models.DateField(null=True, blank=True)
    # age
    sport = models.CharField(max_length=255, blank=True, null=True)
    playing_position = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    objects = BaseUserManager()
    last_login = None
    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'user'
        ordering = ['name']


class Test(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test")
    unit = models.CharField(max_length=255, blank=True, null=True)
    best_score = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'test'
