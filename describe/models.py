from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PersonModel(models.Model):
    user_id = models.ForeignKey(User, unique=True)
    present_description = models.TextField(verbose_name='Opisz swój wymarzony prezent')