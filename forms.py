from django.forms.models import ModelForm
from venture.models import Person

class PersonForm(ModelForm):
 class Meta:
  fields = ['name',]
  model = Person

