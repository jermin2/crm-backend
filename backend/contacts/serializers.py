from rest_framework import serializers
from .models import Person, Family, User

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    family = FamilySerializer()

    class Meta:
        model = Person
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = ['id','email', 'role', 'user_permissions', 'person']