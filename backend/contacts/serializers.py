from rest_framework import serializers
from .models import Person, Family, User
from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer, PasswordResetConfirmSerializer
from .forms import MyCustomResetPasswordForm

class FamilyMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['per_first_name', 'per_last_name', 'per_family_role']

class FamilySerializer(serializers.ModelSerializer):
    family_members = FamilyMembersSerializer( many=True, required=False)

    class Meta:
        model = Family
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    family = FamilySerializer(read_only=True)
    addFamily = serializers.BooleanField(required=False)
    existingFamily = serializers.IntegerField(required=False, allow_null=True)
    fam_name = serializers.CharField(required=False)
    fam_address = serializers.CharField(required=False)
    fam_email = serializers.CharField(required=False)

    class Meta:
        model = Person
        fields = '__all__'

    def to_internal_value(self, data):
        if data.get('per_day_of_birth') == '':
            data['per_day_of_birth'] = None

        if data.get('per_month_of_birth') == '':
            data['per_month_of_birth'] = None

        if data.get('per_year_of_birth') == '':
            data['per_year_of_birth'] = None

        if data.get('existingFamily') == '':
            data['existingFamily'] = None

        return super(PersonSerializer, self).to_internal_value(data)



    def create(self, validated_data):

        addFamily = validated_data.pop('addFamily')
        existing = validated_data.pop('existingFamily')

        def valid_data(key, validated_data):
            if key in validated_data:
                return validated_data.pop(key)
            else:
                return None
        # If we are adding a new family
        if addFamily == True:
            fam_family_name = valid_data('fam_name', validated_data)
            fam_family_email = valid_data('fam_email', validated_data)
            fam_family_address = valid_data('fam_address', validated_data)
            
        person = Person.objects.create(**validated_data)

        if not addFamily:
            person.family = Family.objects.get(id=existing)
            person.save()
        else:
            fam = Family.objects.create(
                fam_family_name=fam_family_name,
                fam_family_email=fam_family_email,
                fam_family_address=fam_family_address
            )
            person.family = fam
            person.save()

        return person



class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = ['id','email', 'role', 'user_permissions', 'person']

class PasswordResetSerializer(_PasswordResetSerializer):
    def validate_email(self, value):
        # I override this line so that I can use MyCustomResetPasswordForm
        self.reset_form = MyCustomResetPasswordForm(data=self.initial_data)  
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value
