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

    ROLES = [('admin', 'Admin'), ('staff', 'Staff'), ('user', 'User')]
    role = models.CharField(max_length=5, choices=ROLES, default='user')

    def __str__(self):
        return self.email


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

