from django.shortcuts import render
from .serializers import PersonSerializer, FamilySerializer, FamilyRoleSerializer
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from .models import Person, Family, FamilyRole

from dj_rest_auth.registration.views import ConfirmEmailView

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

class FamilyView(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all().order_by('fam_familyName')

    def perform_update(self, serializer):
        serializer.save()

# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all().order_by('per_firstName')
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

# class PersonListView(viewsets.ModelViewSet):
#     serializer_class = PersonListSerializer
#     queryset = Person.objects.all().order_by('per_firstName')

class FamilyRoleView(viewsets.ModelViewSet):
    serializer_class = FamilyRoleSerializer
    queryset = FamilyRole.objects.all()

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.role = 'user'
    print("email confirmed")
    user.save()



class CustomConfirmEmailView(ConfirmEmailView):
   pass

