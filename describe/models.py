from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PersonModel(models.Model):
    user_id = models.ForeignKey(User, unique=True)
    present_description = models.TextField(verbose_name='Opisz swoj wymarzony prezent')
    was_choosen = models.BooleanField(default=False)

class RandomizationModel(models.Model):
    user_id = models.IntegerField(unique=True)
    giving = models.IntegerField(unique=True)