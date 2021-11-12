from django.shortcuts import render
from .serializers import PersonSerializer
from rest_framework import viewsets
from .models import Person, Family

# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()