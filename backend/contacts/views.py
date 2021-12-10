from django.shortcuts import render
from .serializers import PersonSerializer, FamilySerializer, FamilyRoleSerializer, AvatarSerializer, UserSerializer, PersonTagSerializer, UserTagSerializer
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from .models import Person, Family, FamilyRole, Avatar, User, Tag
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from dj_rest_auth.registration.views import ConfirmEmailView

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin

class TagView(viewsets.ModelViewSet):
    serializer_class = UserTagSerializer

    def get_queryset(self):
        """
        This view should return a list of tags
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_anonymous:
            print("anonymouse user detected")
            return Tag.objects.all() # TODO - remove this line
        return Tag.objects.filter(user=user)


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

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        Tag.objects.create(color='#ff0000', description='red', user=self)
        Tag.objects.create(color='#00ff00', description='green', user=self)
        Tag.objects.create(color='#0000ff', description='blue', user=self)

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

class PersonTagUpdateView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@api_view(['PUT','PATCH'])
def update_person_tags(request, id):
    # if request.user.is_anonymous:
    #     print("anon")
    #     return JsonResponse({"data":"anonymouse user"}, status=401)

    person = Person.objects.filter(id = id).first()

    tag_id = request.data['tag_id']

    tagData = Tag.objects.filter(tag_id = tag_id).first()
    message = ""
    if person.tags.filter(tag_id = tag_id).exists():
        person.tags.remove(tagData)
        message = "Removed"
    else:
        person.tags.add(tagData)
        message = "Added"
    person.save()

    return JsonResponse({"data":message}, status=200)

@api_view(['PUT','PATCH'])
def update_family_tags(request, id):
    # if request.user.is_anonymous:
    #     print("anon")
    #     return JsonResponse({"data":"anonymouse user"}, status=401)

    family = Family.objects.filter(id = id).first()

    tag_id = request.data['tag_id']

    tagData = Tag.objects.filter(tag_id = tag_id).first()
    message = ""
    if family.tags.filter(tag_id = tag_id).exists():
        family.tags.remove(tagData)
        message = "Removed"
    else:
        family.tags.add(tagData)
        message = "Added"
    family.save()

    return JsonResponse({"data":message}, status=200)

# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT'])
def get_user(request):  

    if request.user.is_anonymous:
        return JsonResponse({"data":"anonymouse user"}, status=401)

    print(request.user)
    serializer = UserSerializer(request.user)
    return JsonResponse({"data":serializer.data}, status=200)
