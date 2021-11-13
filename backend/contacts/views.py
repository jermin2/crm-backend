from django.shortcuts import render
from .serializers import PersonSerializer
from rest_framework import viewsets, permissions
from .models import Person, Family

# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Person.objects.all()