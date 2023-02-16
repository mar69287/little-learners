from django.db import models
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Teacher(models.Model):
  name = models.CharField(max_length=100)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  class Meta:
    permissions = [
      ("is_teacher", "can access teacher views")
    ]

  def __str__(self):
        return self.name

class Child(models.Model):
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=10)
  DoB = models.DateField()
  allergies = models.CharField(max_length=100)
  teacher = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
        return self.name

  def get_absolute_url(self):
    return reverse('teachers_index')
    
class Guardian(models.Model):
  name =  models.CharField(max_length=100)
  relationship = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  zip_code = models.CharField(max_length=5)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  children = models.ManyToManyField(Child)

  def __str__(self):
     return self.name
  
class Task(models.Model):
  name = models.CharField(max_length=20)

  def __str__(self):
      return f"{self.name}" 

  def get_absolute_url(self):
    return reverse('tasks_index')

class AssignActivity(models.Model):
  name = models.CharField(max_length=20)
  child = models.ForeignKey(Child, on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True)

  def __str__(self):
      return f"{self.name}" 

  class Meta:
    ordering = ['-date']
   
class Feeding(models.Model):
  did_eat= models.CharField(max_length=20)
  child = models.ForeignKey(Child, on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True)

  def __str__(self):
    return f"child {self.did_eat} on {self.date}"

  class Meta:
    ordering = ['-date']

class Attendance(models.Model):
  child = models.ForeignKey(Child, on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True) 
  status = models.CharField(max_length=10)

  def __str__(self):
    return f"{self.status} on {self.date}"

  class Meta:
    ordering = ['-date']

class Assessment(models.Model):
  behavior = models.CharField(max_length=10)
  date = models.DateField(auto_now_add=True)
  child = models.ForeignKey(Child, on_delete=models.CASCADE)

  def __str__(self):
        return f"{self.behavior} on {self.date}"

  class Meta:
    ordering = ['-date']

class Comment(models.Model):
  message = models.TextField(max_length=200)
  date = models.DateTimeField(auto_now_add=True)
  child = models.ForeignKey(Child, on_delete=models.CASCADE)

  def __str__(self):
        return f"{self.message} on {self.date}"

  class Meta:
    ordering = ['-date']