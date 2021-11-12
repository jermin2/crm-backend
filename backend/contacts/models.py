from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=255)
    last_name = models.CharField( max_length=255)
    family = models.ForeignKey( 'Family', null=True, blank=True, on_delete=models.CASCADE, related_name="family_members" )

    def __str__(self):
        return self.last_name.upper() + " " + self.first_name 

class Family(models.Model):
    family_name = models.CharField( max_length=255)

    def __str__(self):
        return str(self.id) + "|" + self.family_name.upper()
