from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PersonModel(models.Model):
    user_id = models.ForeignKey(User, unique=True)
    present_description = models.TextField(verbose_name='Opisz swoj wymarzony prezent')

    def present_desc(self):
        return self.present_description

    def get_user_name(self):
        return PersonModel.get_user_name_static(self.user_id)

    @staticmethod
    def get_user_name_static(user):
        return user.first_name + " " + user.last_name

    def __str__(self):
        return self.get_user_name()

    def __eq__(self, other):
        return  self.user_id == other.user_id

    def __ne__(self, other):
        return not self.user_id == other.user_id

class RandomizationModel(models.Model):
    user_id = models.IntegerField(unique=True)
    giving_id = models.IntegerField(unique=True)

    def __str__(self):
        me = User.objects.get(pk=self.user_id)
        giving_person = User.objects.get(pk=self.giving_id)
        str = PersonModel.get_user_name_static(me) + " -> " + PersonModel.get_user_name_static(giving_person)
        return str

    def __eq__(self, other):
        return  self.user_id == other.user_id and self.giving_id == other.giving

    def __ne__(self, other):
        return self.user_id != other.user_id or self.giving_id != other.giving