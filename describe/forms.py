from django import forms
from describe.models import PersonModel

class PersonForm(forms.ModelForm):
    class Meta:
        model = PersonModel
        fields = ('present_description',)
