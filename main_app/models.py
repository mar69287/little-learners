from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone


MEALS = (
  ('B', 'Breakfast - 9:00 am - 9:30 am'),
  ('L', 'Lunch - 12:00 pm - 12:30 pm'),
  ('S', 'Snack - 2:00 pm - 2:30 pm'),
  
)

ATE = (
    ('N', 'No'),
    ('Y', 'Yes')
)

ACTIONS = (
  ('C', 'Coloring'),
  ('M', 'Music'),
  ('N', 'Nap'),
  ('R', 'Reading'),
  ('P', 'Play'),
  ('W', 'Writing'),
  
)

class Teacher(models.Model):
  name = models.CharField(max_length=100)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

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
  
class Activity(models.Model):
   action = models.CharField(
      max_length=1,
      choices=ACTIONS,
      default=ACTIONS[0][0]
   )
   start_time = models.DateTimeField(blank=True, null=True, default=timezone.now)
   end_time = models.DateTimeField(blank=True, null=True, )
   comment = models.CharField(max_length=250)

   def __str__(self):
      return f"{self.get_action_display()} from {self.start_time} to {self.end_time}"
   
class Feeding(models.Model):
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  ),
  did_eat= models.CharField(
    max_length=1,
    choices=ATE,
    default=ATE[1][0]
  ),
  def __str__(self):
    return f"child at {self.get_meal_display()} ate? {self.get_did_eat_display()}"

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