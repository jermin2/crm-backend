from rest_framework import serializers
from .models import Person, Family, User, FamilyRole
from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer, PasswordResetConfirmSerializer
from .forms import MyCustomResetPasswordForm
import datetime

class FamilyMembersSerializer(serializers.ModelSerializer):
    family_role_text = serializers.SerializerMethodField(required=False)
    per_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['per_first_name', 'per_last_name', 'per_family_role', 'family_role_text']

    
    def get_family_role_text(self,obj):
        if obj.per_family_role:
            return obj.per_family_role.family_role
        else :
            return "Not set"

    def get_per_last_name(self, obj):
        if obj.per_last_name:
            return obj.per_last_name
        else :
            return obj.family.fam_family_name

class FamilySerializer(serializers.ModelSerializer):
    family_members = FamilyMembersSerializer( many=True, required=False, read_only=True)
    family_id = serializers.IntegerField(required=False)

    class Meta:
        model = Family
        fields = ['id', 'family_id', 'fam_family_name', 'fam_family_email', 'fam_family_address', 'family_members']

    def to_internal_value(self, data):
        #use existing family
        if data['addFamily'] == "false": 
            try:
                obj_id = data['id']
                return Family.objects.get(id=obj_id)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        else:
            # Create new family
            family_data = super(FamilySerializer, self).to_internal_value(data)
            return Family.objects.create(**family_data)


    # def update(self, instance, validated_data):
    #     print(validated_data)

class PersonSerializer(serializers.ModelSerializer):
    family = FamilySerializer(required=False)
    school_year = serializers.SerializerMethodField(required=False)

    per_last_name = serializers.SerializerMethodField()
    age_group = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'

    def to_internal_value(self, data):

        # Convert school year to per_year_one_year
        if data.get('school_year') == '':
            data['school_year'] = None
        else:
            data['per_year_one_year'] = self.reverseSchoolYear( int(data.get('school_year')) )

        return super(PersonSerializer, self).to_internal_value(data)

    def reverseSchoolYear(self, schoolYear):
        if schoolYear > 1000:
            return schoolYear - 13
        else:
            return datetime.datetime.now().year - schoolYear
        
    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     schoolYear = validated_data.pop('school_year')
    #     # Set correct year one
    #     if schoolYear:
    #         validated_data['per_year_one_year'] = self.reverseSchoolYear (int(schoolYear))
    #     validated_data.pop('existingFamily')
    #     validated_data.pop('set_school_year')
    #     validated_data.pop('age_group')

    #     person = Person.objects.filter(id=instance.id).update(**validated_data)

    #     return person

    def create(self, validated_data):
        person = Person.objects.create(**validated_data)
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

    # Return family last name, if none is entered
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