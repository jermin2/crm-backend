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
    queryset = Family.objects.all()

# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Person.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    # def update(self, request, pk=None):
    #     print(self.request.data)

    def perform_update(self, serializer):
        person = Person.objects.get(id = self.request.data.get('id'))

        # Get family data
        family_data = self.request.data.pop('family')
        family = Family.objects.get(id = family_data.get('id'))

        # Update family data
        family_serializer = FamilySerializer(data=family_data)
        family_serializer.is_valid()
        if 'family_members' in family_data:
            family_data.pop('family_members') # family_members field should be read only
        family_serializer.update(family, family_data)

        person.family = family

        # Update Family Role
        per_family_role_data = self.request.data.pop('per_family_role')
        family_role = FamilyRole.objects.get(id = per_family_role_data)
        person.per_family_role = family_role
        
        serializer.update(person, self.request.data)


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

