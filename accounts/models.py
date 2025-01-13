from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=False, default='a@a.com')

    def __str__(self):
        return self.username