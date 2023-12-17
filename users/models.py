from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    chat_id = models.CharField(max_length=100, verbose_name='chat_id', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
