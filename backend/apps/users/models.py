from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pseudo = models.CharField(
        max_length=150,
        blank=True,
        help_text="Display name for the user."
    )

    def __str__(self):
        return self.username
