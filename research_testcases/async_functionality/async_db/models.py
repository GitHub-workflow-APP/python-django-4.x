from django.forms import ModelForm
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=96)
    phone_number = models.CharField(max_length=12)

