from rest_framework import serializers
from .models import Person, Family

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    family = FamilySerializer()

    class Meta:
        model = Person
        fields = '__all__'

