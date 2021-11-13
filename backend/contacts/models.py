from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# Create your models here.
class User(AbstractUser):
    ROLES = [('admin', 'Admin'), ('staff', 'Staff'), ('user', 'User')]
    role = models.CharField(max_length=5, choices=ROLES, default='user')


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person")
    first_name = models.CharField( max_length=255)
    last_name = models.CharField( max_length=255)
    family = models.ForeignKey( 'Family', null=True, blank=True, on_delete=models.CASCADE, related_name="family_members" )

    def __str__(self):
        return self.last_name.upper() + " " + self.first_name 

    @property
    def displayName(self):
        return self.first_name.title() + " " + self.last_name.title()

class Family(models.Model):
    family_name = models.CharField( max_length=255)

    def __str__(self):
        return str(self.id) + "|" + self.family_name.upper()

