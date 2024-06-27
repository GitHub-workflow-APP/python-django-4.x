from django.forms import ModelForm
from .models import Person

class SubscribeForm(ModelForm):
    class Meta:
        model = Person
        fields = {'name', 'phone_number'}
