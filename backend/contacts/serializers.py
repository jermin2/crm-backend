from rest_framework import serializers
from .models import Person, Family

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person