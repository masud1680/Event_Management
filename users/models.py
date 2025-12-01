from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, default='not-found-icon-4.jpg' )
    bio = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=500, blank=True)
    gender = models.CharField(blank=True)
    age = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    blood_group = models.CharField(max_length=3, blank=True)


    def __str__(self):
        return self.username