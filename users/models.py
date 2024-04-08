from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    profile_pictures = models.ImageField(upload_to='users_profile/', null=True, blank=True, default='users_profile/default-profile-pic.png')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


