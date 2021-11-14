from django.shortcuts import render
from .serializers import PersonSerializer
from rest_framework import viewsets, permissions
from .models import Person, Family

from dj_rest_auth.registration.views import ConfirmEmailView

from allauth.account.signals import email_confirmed
from django.dispatch import receiver


# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Person.objects.all()


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.role = 'user'
    print("email confirmed")
    user.save()



class CustomConfirmEmailView(ConfirmEmailView):
   pass