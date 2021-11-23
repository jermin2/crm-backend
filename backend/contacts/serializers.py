from rest_framework import serializers
from .models import Person, Family, User, FamilyRole
from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer, PasswordResetConfirmSerializer
from .forms import MyCustomResetPasswordForm
import datetime

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
    fam_name = serializers.CharField(required=False, allow_blank=True)
    fam_address = serializers.CharField(required=False, allow_blank=True)
    fam_email = serializers.CharField(required=False, allow_blank=True)
    set_school_year = serializers.IntegerField(required=False, allow_null=True)
    school_year = serializers.SerializerMethodField(required=False)
    per_last_name = serializers.SerializerMethodField()
    age_group = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'

    def to_internal_value(self, data):
        if data.get('existingFamily') == '':
            data['existingFamily'] = None

        if data.get('set_school_year') == '':
            data['set_school_year'] = None

        return super(PersonSerializer, self).to_internal_value(data)



    def create(self, validated_data):
        print(validated_data)

        def valid_data(key, validated_data):
            if key in validated_data:
                return validated_data.pop(key)
            else:
                return None

        schoolYear = valid_data('set_school_year', validated_data)
        addFamily = valid_data('addFamily', validated_data)
        existing = valid_data('existingFamily', validated_data)
        fam_family_name = valid_data('fam_name', validated_data)
        fam_family_email = valid_data('fam_email', validated_data)
        fam_family_address = valid_data('fam_address', validated_data)


        # Set correct year one
        if schoolYear:
            if schoolYear > 1000:
                validated_data['per_year_one_year'] = schoolYear - 13
            else:
                validated_data['per_year_one_year'] = datetime.datetime.now().year - schoolYear
            
            
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

    def get_school_year(self, obj):
        if obj.per_year_one_year:
            school_year = datetime.datetime.now().year - obj.per_year_one_year
            if school_year < 13 :
                return (datetime.datetime.now().year - obj.per_year_one_year)
            else:
                return obj.per_year_one_year + 13
        return None

    def get_age_group(self, obj):
        if obj.per_year_one_year:
            return "To Be Implemented"
        return "Please set school / graduation year"

    def get_per_last_name(self, obj):
        if obj.per_last_name:
            return obj.per_last_name
        else :
            return obj.family.fam_family_name



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

class FamilyRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = FamilyRole
        fields = '__all__'