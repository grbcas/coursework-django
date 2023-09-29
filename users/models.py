from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=150, **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='email address')
    comment = models.TextField(max_length=200, **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='is_verified')

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
