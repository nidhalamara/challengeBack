from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class VUserManager(BaseUserManager):
    def create_user(self, cin, name, password=None, **extra_fields):
        """
        Creates and saves a V_USER with the given CIN, name, and password.
        """


        user = self.model(cin=cin, name=name, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, cin, name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given CIN, name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(cin, name, password, **extra_fields)


class VUser(AbstractBaseUser, PermissionsMixin):
    cin = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    objects = VUserManager()

    USERNAME_FIELD = 'cin'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.cin
