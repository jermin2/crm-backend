from django.shortcuts import render
from .serializers import PersonSerializer, FamilySerializer
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from .models import Person, Family

from dj_rest_auth.registration.views import ConfirmEmailView

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

class FamilyView(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all()

# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Person.objects.all()

    # def perform_create(self, serializer):
    #     print(self.request.data)
    #     serializer.save(person=self.request.data)

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.role = 'user'
    print("email confirmed")
    user.save()



class CustomConfirmEmailView(ConfirmEmailView):
   pass