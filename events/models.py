from django.db import models

# Create your models here.
class ParticipantModel(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    
    def __str__(self):
         return self.name
     
class EventModel(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    date = models.DateField( )
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey("CategoryModel", related_name="eventC", on_delete=models.CASCADE , default=1)
    assigned_to = models.ManyToManyField(ParticipantModel, related_name="eventP" )

    def __str__(self):
        return self.name


      
class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    
    def __str__(self):
         return self.name