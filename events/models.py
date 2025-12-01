from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

     
class EventModel(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateField( )
    time = models.TimeField()
    location = models.CharField(max_length=200)
    Easset = models.ImageField(upload_to="events_asset/", blank=True, null=True, default='not-found-icon-4.jpg')
    category = models.ForeignKey("CategoryModel", related_name="eventC", on_delete=models.CASCADE , default=1)
    Participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="eventP" )

    def __str__(self):
        return self.name


      
class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    Casset = models.ImageField(upload_to="categorys_asset/", blank=True, null=True, default='not-found-icon-4.jpg')
    
    def __str__(self):
         return self.name