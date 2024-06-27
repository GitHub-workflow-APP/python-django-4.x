from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(
        max_length=200, null=False, default='')
    last_name = models.CharField(
        max_length=200, null=False, default='')
    email = models.EmailField(
        max_length=70, null=True, default='')

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name
