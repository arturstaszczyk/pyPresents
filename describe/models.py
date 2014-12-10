from django.db import models

# Create your models here.

class PersonModel(models.Model):
    user_id = models.ForeignKey('auth.User')
    present_description = models.TextField()