from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class CustomUserManager(BaseUserManager):
    """
    Custom user model where email is unique identifier for authentication instead of usernames
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    ROLES = [('admin', 'Admin'), ('staff', 'Staff'), ('user', 'User'),('unverified', 'Unverified'),('guest', 'Guest')]
    role = models.CharField(max_length=10, choices=ROLES, default='unverified')

    def __str__(self):
        return self.email


class FamilyRole(models.Model):
    family_role = models.CharField( max_length=20 )

    def __str__(self):
        return self.family_role

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person", null=True, blank=True)
    per_firstName = models.CharField( max_length=255)
    per_lastName = models.CharField( max_length=255, default='', blank=True)
    per_phone = models.CharField( max_length=20, default='', blank=True)
    per_email = models.EmailField(_('email address'), default='', blank=True)
    per_birthday = models.DateField(null=True, blank=True)
    per_yearOneYear = models.IntegerField(null=True, blank=True)
    per_familyRole = models.ForeignKey(FamilyRole, on_delete=models.CASCADE, default=1)
    family = models.ForeignKey( 'Family', null=True, blank=True, on_delete=models.CASCADE, related_name="family_members" )

    def __str__(self):
        return self.per_lastName.upper() + " " + self.per_firstName 

    @property
    def displayName(self):
        return self.per_firstName.title() + " " + self.per_lastName.title()

class Family(models.Model):
    fam_familyName = models.CharField( max_length=255)
    fam_familyAddress = models.CharField( max_length=500, default='', blank=True)
    fam_familyEmail = models.EmailField(_('email address'), default='', blank=True)

    def __str__(self):
        return str(self.id) + "|" + self.fam_familyName.upper()

