from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    occupants_count = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Business(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hood = models.ForeignKey(Hood,on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name
