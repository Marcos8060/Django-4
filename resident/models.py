from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Business(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Hood(models.Model):
    business = models.ForeignKey(Business,on_delete=models.CASCADE,default='Airtel')
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    occupants_count = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hood',default='../images/neighbour.jpg')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('details',args=[self.id])


