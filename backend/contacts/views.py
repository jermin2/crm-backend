from django.shortcuts import render
from .serializers import PersonSerializer, FamilySerializer, FamilyRoleSerializer, AvatarSerializer, UserSerializer
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from .models import Person, Family, FamilyRole, Avatar, User
from rest_framework.decorators import api_view, authentication_classes, permission_classes

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
        print(self.request.data)
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

class AvatarView(viewsets.ModelViewSet):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()

class CustomConfirmEmailView(ConfirmEmailView):
   pass


# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT'])
def get_user(request):  

    if request.user.is_anonymous:
        return JsonResponse({"data":"anonymouse user"}, status=401)

    print(request.user)
    serializer = UserSerializer(request.user)
    return JsonResponse({"data":serializer.data}, status=200)
