from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Teacher(models.Model):
  name = models.CharField(max_length=100)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
        return self.name
    
class Guardian(models.Model):
  name =  models.CharField(max_length=100)
  relationship = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=5)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
     return self.name
  
class Child(models.Model):
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=10)
  DoB = models.DateField()
  allergies = models.CharField(max_length=100)
  guardians = models.ManyToManyField(Guardian)

  def __str__(self):
        return self.name

  def get_absolute_url(self):
    return reverse('guardians_index', kwargs ={'pk': self.id})